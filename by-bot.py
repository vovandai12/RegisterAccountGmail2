from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import os
import zipfile
import time
import random
import traceback
import string
import requests
import json


WAIT = random.randint(15, 30)
DELAY = random.randint(10, 30) / 10.0
PROXY = "95.164.206.82:8080:e12582:proxy11"

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (
    PROXY.split(":")[0],
    PROXY.split(":")[1],
    PROXY.split(":")[2],
    PROXY.split(":")[3],
)


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


class Proxyfb:
    def __init__(self, data=None):
        if data is not None:
            self.success = data.get("success", None)
            self.proxy = data.get("proxy", None)
            self.location = data.get("location", None)
            self.next_change = data.get("next_change", None)
            self.timeout = data.get("timeout", None)


def buy_phone_number(key):
    try:
        url = f"https://api.viotp.com/request/getv2?token={key}&serviceId=3"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if result["status_code"] == 200:
            if result["data"]:
                return Viotp(result["data"])
        return None
    except:
        return None


def get_otp(key, id_phone):
    try:
        url = f"https://api.viotp.com/session/getv2?requestId={id_phone}&token={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if result["status_code"] == 200:
            if result["data"]:
                return ViotpSMS(result["data"])
        return None
    except:
        return None


def generatePhone():
    try:
        phone = None
        id_phone = None
        key = "d2e5c07f49f14006a1fcde8427a77115"
        value = "viotp"
        if value == "viotp":
            buy_phone = buy_phone_number(key)
            if buy_phone:
                phone = "0" + buy_phone.phone_number
                id_phone = buy_phone.request_id
        return phone, id_phone
    except:
        return None, None


def generateCode(id_phone):
    try:
        code = None
        key = "d2e5c07f49f14006a1fcde8427a77115"
        value = "viotp"
        if value == "viotp":
            by_code = get_otp(key, id_phone)
            if by_code:
                code = by_code.Code
        return code
    except:
        return None


def get_proxy(key):
    proxyfb = None
    try:
        url = f"http://api.proxyfb.com/api/changeProxy.php?key={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if "success" in result:
            if result["success"]:
                proxyfb = Proxyfb(result)
                return proxyfb
        return proxyfb
    except:
        return None


def generateProxy():
    try:
        proxy = None
        key = [
            "1b16a593b7d1f94706acc708f016bd6b",
        ]
        value = "proxyfb"
        for item in key:
            if value == "proxyfb":
                by_proxy = get_proxy(item)
                if by_proxy:
                    proxy = by_proxy.proxy
                    break
        if proxy is not None:
            return proxy
        return None
    except:
        return None


options = webdriver.ChromeOptions()
options = Options()
PROXY_2 = None
count = 1
while count <= 15:
    by_proxy = generateProxy()
    if by_proxy:
        PROXY_2 = by_proxy
        break
    time.sleep(5)
    count += 1
print(f"PROXY_2->{PROXY_2}")
options.add_argument("--proxy-server=%s" % PROXY_2)
path_plugin = os.path.dirname(os.path.abspath(__file__))
pluginfile = "proxy_auth_plugin.zip"
with zipfile.ZipFile(pluginfile, "w") as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
    # options.add_extension(pluginfile)
options.add_argument("--app=http://www.google.com")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
#
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("disable-popup-blocking")
options.add_argument("disable-notifications")
options.add_argument("disable-popup-blocking")
options.add_argument("--ignore-ssl-errors=yes")
options.add_argument("--ignore-certificate-errors")
prefs = {
    "profile.password_manager_enabled": False,
    "credentials_enable_service": False,
    "useAutomationExtension": False,
}
options.add_experimental_option("prefs", prefs)
#
user_agent = UserAgent(
    fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
).random
options.add_argument(f"user-agent={user_agent}")
#
# driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(
#     service=Service(
#         executable_path=r"E:\Github\SeleniumAndGologin\ChromeDriver\chromedriver.exe"
#     ),
#     options=options,
# )
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.set_window_rect(0, 0, 800, 600)
driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
)
# user_agent = UserAgent(
#     fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
# ).random
# driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
# driver.get("chrome://version")
# time.sleep(15)
# driver.get("https://mail.google.com/")
# time.sleep(DELAY)
# time.sleep(5)
# driver.get("https://httpbin.org/ip")
# time.sleep(50)
time.sleep(DELAY)
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Gmail')]"))
    ).click()
except Exception as e:
    traceback.print_exc()
    driver.quit()
time.sleep(DELAY)
try:
    WebDriverWait(driver, WAIT / 2).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Đăng nhập')]"))
    ).click()
except Exception as e:
    pass
    # traceback.print_exc()
    # driver.quit()
time.sleep(DELAY)
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Loại bỏ')]"))
    ).click()
except Exception as e:
    pass
# time.sleep(DELAY)
# driver.execute_script('window.scrollTo(0, 600)')
time.sleep(DELAY)
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
            )
        )
    ).click()
except Exception as e:
    traceback.print_exc()
    driver.quit()
time.sleep(DELAY)
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'Dành cho mục đích cá nhân của tôi')]")
        )
    ).click()
except Exception as e:
    traceback.print_exc()
    driver.quit()

last_name = "Huỳnh Thị Thuý"
first_name = "Nga"
print(f"##### IMPORT FULLNAME - {first_name} {last_name} #####")
print(f"####- IMPORT LASTNAME - {last_name} -####")
time.sleep(DELAY)
try:
    element_lastName = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='lastName']"))
    )
    for char in last_name:
        element_lastName.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_lastName.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
print(f"####- IMPORT FIRSTNAME - {first_name} -####")
try:
    element_firstName = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='firstName']"))
    )
    for char in first_name:
        element_firstName.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_firstName.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()

birthday = (
    str(random.randint(1, 28))
    + "/"
    + str(random.randint(1, 12))
    + "/"
    + str(random.randint(1980, 2004))
)
gender = random.randint(1, 2)
print(f"##### IMPORT BIRTHDAY - {birthday} AND GENDER - {gender} #####")
print(f"####- IMPORT DAY - {birthday.split('/')[0]} -####")
time.sleep(DELAY)
try:
    element_day = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="day"]'))
    )
    element_day.click()
    for char in birthday.split("/")[0]:
        element_day.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
except Exception as e:
    traceback.print_exc()
    driver.quit()
print(f"####- IMPORT MONTH - {birthday.split('/')[1]} -####")
time.sleep(DELAY)
try:
    element_month = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="month"]'))
    )
    element_month.click()
    for _ in range(1, int(birthday.split("/")[1]) + 1):
        element_month.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1 + 0.1 * random.random())
    element_month.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
print(f"####- IMPORT YEAR - {birthday.split('/')[2]} -####")
time.sleep(DELAY)
try:
    element_year = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="year"]'))
    )
    element_year.click()
    for char in birthday.split("/")[2]:
        element_year.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
except Exception as e:
    traceback.print_exc()
    driver.quit()
print(f"####- IMPORT GENDER - {gender} -####")
time.sleep(DELAY)
try:
    element_gender = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="gender"]'))
    )
    element_gender.click()
    for _ in range(1, gender + 1):
        element_gender.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.1 + 0.1 * random.random())
    element_gender.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
######
time.sleep(DELAY)
try:
    WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
            )
        )
    ).click()
except Exception as e:
    traceback.print_exc()
    driver.quit()
time.sleep(DELAY)
try:
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Thay vào đó hãy lấy địa chỉ Gmail')]")
        )
    ).click()
except:
    pass
time.sleep(DELAY)
try:
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(text(),'Tạo địa chỉ Gmail của riêng bạn')]")
        )
    ).click()
except:
    pass
username = f"huynh.thi.thuy.nga.{birthday.split('/')[0]}{birthday.split('/')[1]}{birthday.split('/')[2]}"
print(f"##### IMPORT USERNAME - {username} #####")
print(f"####- IMPORT USERNAME - {username} -####")
time.sleep(DELAY)
try:
    element_username = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='Username']"))
    )
    element_username.click()
    for char in username:
        element_username.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_username.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
chars_password = (
    string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
)
size_password = random.randint(10, 20)
password = "".join(random.choice(chars_password) for x in range(size_password))
print(f"##### IMPORT PASSWORD AND CONFIRMPASSWROD - {password} #####")
print(f"####- IMPORT PASSWORD - {password} -####")
time.sleep(DELAY)
try:
    element_passwd = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='Passwd']"))
    )
    for char in password:
        element_passwd.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_passwd.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
print(f"####- IMPORT CONFIRMPASSWROD - {password} -####")
time.sleep(DELAY)
try:
    element_passwd_again = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//*[@name='PasswdAgain']"))
    )
    for char in password:
        element_passwd_again.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_passwd_again.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()

phone = None
id_phone = None
while True:
    count = 1
    while count <= 15:
        by_phone, by_id_phone = generatePhone()
        if by_phone and by_id_phone:
            phone = by_phone
            id_phone = by_id_phone
            break
        time.sleep(5)
        count += 1
    print(f"##### IMPORT PHONENUMBER - {phone} - {id_phone} #####")
    print(f"####- IMPORT PHONENUMBER - {phone} -####")
    try:
        element_phone = WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='phoneNumberId']"))
        )
        text_length = len(element_phone.get_attribute("value"))
        if text_length > 0:
            for _ in range(text_length):
                element_phone.send_keys(Keys.ARROW_LEFT)
                time.sleep(0.1 + 0.1 * random.random())
                element_phone.send_keys(Keys.DELETE)
        for char in phone:
            element_phone.send_keys(char)
            time.sleep(0.1 + 0.1 * random.random())
        element_phone.send_keys(Keys.ENTER)
    except Exception as e:
        traceback.print_exc()
        driver.quit()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="code"]'))
        )
        break
    except:
        pass

code = None
count = 1
while count <= 15:
    by_code = generateCode(id_phone)
    if by_code:
        code = by_code
        break
    time.sleep(5)
    count += 1
print(f"##### IMPORT CODE - {code} #####")
print(f"####- IMPORT CODE - {code} -####")
try:
    element_code = WebDriverWait(driver, WAIT).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="code"]'))
    )
    for char in code:
        element_code.send_keys(char)
        time.sleep(0.1 + 0.1 * random.random())
    element_code.send_keys(Keys.ENTER)
except Exception as e:
    traceback.print_exc()
    driver.quit()
recovery = False
if recovery:
    email_recovery = "kemcaysacacam556731@gmail.com"
    if email_recovery:
        print(f"##### IMPORT EMAIL RECOVERY - {email_recovery} #####")
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="recovery"]'))
        ).send_keys(email_recovery)
        time.sleep(DELAY)
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Next')]")
            )
        ).click()
        time.sleep(DELAY)
    else:
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Skip')]")
            )
        ).click()
        time.sleep(DELAY)
else:
    try:
        WebDriverWait(driver, WAIT).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(text(),'Skip')]")
            )
        ).click()
        time.sleep(DELAY)
    except:
        pass


####### Bật POP/IMAP
# kiểm tra title Hộp thư đến - huynh.thi.thuy.nga.7101991@gmail.com - Gmail
# xem email click span Nhóm phụ trách cộng.
# quay lại click div ar6 T-I-J3 J-J5-Ji
# mở cài đặt <div class="FI" data-tooltip="Cài đặt" jslog="85046; u014N:cOuCgd,Kr2w4b,xr6bB;"><a class="FH" role="button" tabindex="0" aria-label="Cài đặt"><svg class="Xy" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M13.85 22.25h-3.7c-.74 0-1.36-.54-1.45-1.27l-.27-1.89c-.27-.14-.53-.29-.79-.46l-1.8.72c-.7.26-1.47-.03-1.81-.65L2.2 15.53c-.35-.66-.2-1.44.36-1.88l1.53-1.19c-.01-.15-.02-.3-.02-.46 0-.15.01-.31.02-.46l-1.52-1.19c-.59-.45-.74-1.26-.37-1.88l1.85-3.19c.34-.62 1.11-.9 1.79-.63l1.81.73c.26-.17.52-.32.78-.46l.27-1.91c.09-.7.71-1.25 1.44-1.25h3.7c.74 0 1.36.54 1.45 1.27l.27 1.89c.27.14.53.29.79.46l1.8-.72c.71-.26 1.48.03 1.82.65l1.84 3.18c.36.66.2 1.44-.36 1.88l-1.52 1.19c.01.15.02.3.02.46s-.01.31-.02.46l1.52 1.19c.56.45.72 1.23.37 1.86l-1.86 3.22c-.34.62-1.11.9-1.8.63l-1.8-.72c-.26.17-.52.32-.78.46l-.27 1.91c-.1.68-.72 1.22-1.46 1.22zm-3.23-2h2.76l.37-2.55.53-.22c.44-.18.88-.44 1.34-.78l.45-.34 2.38.96 1.38-2.4-2.03-1.58.07-.56c.03-.26.06-.51.06-.78s-.03-.53-.06-.78l-.07-.56 2.03-1.58-1.39-2.4-2.39.96-.45-.35c-.42-.32-.87-.58-1.33-.77l-.52-.22-.37-2.55h-2.76l-.37 2.55-.53.21c-.44.19-.88.44-1.34.79l-.45.33-2.38-.95-1.39 2.39 2.03 1.58-.07.56a7 7 0 0 0-.06.79c0 .26.02.53.06.78l.07.56-2.03 1.58 1.38 2.4 2.39-.96.45.35c.43.33.86.58 1.33.77l.53.22.38 2.55z"></path><circle cx="12" cy="12" r="3.5"></circle></svg></a></div>
# click button Xem tất cả chế độ cài đặt
# click a Chuyển tiếp và POP/IMAP
# click <label for=":i3">Bật POP cho <span class="rQ">tất cả thư</span></label>
# click <label for=":mr">Bật IMAP</label>
# click <button id=":h6" guidedhelpid="save_changes_button">Lưu thay đổi</button>

time.sleep(15)
