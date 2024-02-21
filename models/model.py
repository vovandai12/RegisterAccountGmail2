from datetime import datetime


class Account:
    def __init__(
        self,
        username=None,
        password=None,
        recoveryEmail=None,
        firstName=None,
        lastName=None,
        birthDay=None,
        gender=None,
        phone=None,
        idPhone=None,
        proxy=None,
    ):
        self.username = username
        self.password = password
        self.recoveryEmail = recoveryEmail
        self.firstName = firstName
        self.lastName = lastName
        self.birthDay = birthDay
        self.gender = gender
        self.phone = phone
        self.idPhone = idPhone
        self.proxy = proxy
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.createDate = dt_string


class Tmproxy:
    def __init__(self, data=None):
        if data is not None:
            self.ip_allow = data.get("ip_allow", None)
            self.location_name = data.get("location_name", None)
            self.socks5 = data.get("socks5", None)
            self.https = data.get("https", None)
            self.timeout = data.get("timeout", None)
            self.next_request = data.get("next_request", None)
            self.expired_at = data.get("expired_at", None)


class Proxyfb:
    def __init__(self, data=None):
        if data is not None:
            self.success = data.get("success", None)
            self.proxy = data.get("proxy", None)
            self.location = data.get("location", None)
            self.next_change = data.get("next_change", None)
            self.timeout = data.get("timeout", None)


class ProxyShopLike:
    def __init__(self, data=None):
        if data is not None:
            self.location = data.get("location", None)
            self.proxy = data.get("proxy", None)
            self.auth = data.get("auth", None)
            self.nextChange = data.get("nextChange", None)
            self.proxyTimeout = data.get("proxyTimeout", None)


class Ironsim:
    def __init__(self, data=None):
        if data is not None:
            self.phone_number = data.get("phone_number", None)
            self.network = data.get("network", None)
            self.session = data.get("session", None)
            self.id = data.get("id", None)
            self.service_id = data.get("service_id", None)
            self.service_name = data.get("service_name", None)
            self.status = data.get("status", None)
            self.messages = data.get("messages", None)


class BossOtp:
    def __init__(self, data=None):
        if data is not None:
            self.rent_id = data.get("rent_id", None)
            self.status_description = data.get("status_description", None)
            self.sim_id = data.get("sim_id", None)
            self.number = data.get("number", None)
            self.sms_content = data.get("sms_content", None)


class Viotp:
    def __init__(self, data=None):
        if data is not None:
            self.phone_number = data.get("phone_number", None)
            self.re_phone_number = data.get("re_phone_number", None)
            self.countryISO = data.get("countryISO", None)
            self.countryCode = data.get("countryCode", None)
            self.request_id = data.get("request_id", None)
            self.balance = data.get("balance", None)


class ViotpSMS:
    def __init__(self, data=None):
        self.ID = data.get("ID", None)
        self.ServiceID = data.get("ServiceID", None)
        self.ServiceName = data.get("ServiceName", None)
        self.Price = data.get("Price", None)
        self.SmsContent = data.get("SmsContent", None)
        self.Status = data.get("Status", None)
        self.CreatedTime = data.get("CreatedTime", None)
        self.IsSound = data.get("IsSound", None)
        self.Code = data.get("Code", None)
        self.PhoneOriginal = data.get("PhoneOriginal", None)
        self.Phone = data.get("Phone", None)
        self.CountryISO = data.get("CountryISO", None)
        self.CountryCode = data.get("CountryCode", None)


class Simotp:
    def __init__(self, data=None):
        if data is not None:
            self.id = data.get("id", None)
            self.phoneNumber = data.get("phoneNumber", None)
            self.provider = data.get("provider", None)
            self.serviceName = data.get("serviceName", None)
            self.content = data.get("content", None)
            self.status = data.get("status", None)
            self.createdAt = data.get("createdAt", None)
            

class Hcotp:
    def __init__(self, data=None):
        if data is not None:
            self.id = data.get("id", None)
            self.serviceId = data.get("serviceId", None)
            self.carrierName = data.get("carrierName", None)
            self.phoneNum = data.get("phoneNum", None)
            self.requestTime = data.get("requestTime", None)
            self.status = data.get("status", None)
            self.endTime = data.get("endTime", None)
            self.code = data.get("code", None)
            self.message = data.get("message", None)
            self.groupId = data.get("groupId", None)
            self.reuse = data.get("reuse", None)
            self.gsmName = data.get("gsmName", None)
            self.amount = data.get("amount", None)
            self.userName = data.get("userName", None)
            self.responseTime = data.get("responseTime", None)
            self.guidId = data.get("guidId", None)
