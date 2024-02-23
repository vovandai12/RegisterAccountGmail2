from threading import Thread, Event
from datetime import datetime
import traceback
import config as config
from config import SUCCESS, ERROR, RUN
import time
import random
import services.service as ServiceBot
from file_paths import FilePaths
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

totail_error = 0
totail_success = 0


class Bot:
    def __init__(self, config={}):
        self.insert_account_event = lambda v: v
        self.update_account_event = lambda v: v
        self.update_error_event = lambda v: v
        self.update_success_event = lambda v: v
        self.stop_event = Event()

    def Stop(self):
        try:
            self.stop_event.set()
        except Exception as e:
            traceback.print_exc()

    def Start(self):
        try:
            global totail_error
            totail_error = 0
            global totail_success
            totail_success = 0
            self.update_error_event(totail_error)
            self.update_success_event(totail_success)
            number_thread = int(config.global_config.numberThread)
            for index in range(0, number_thread):
                thread = Thread(target=self.DoWorker, args=(index,))
                thread.daemon = True
                thread.start()
            print("main done")
        except Exception as e:
            traceback.print_exc()

    def DoWorker(self, index):
        global totail_error
        global totail_success
        count_event = 0
        while not self.stop_event.is_set():
            count_event += 1
            driver = None
            account = None
            self.update_error_event(totail_error)
            self.update_success_event(totail_success)
            number_acc = int(config.global_config.numberAccount)
            if totail_success >= number_acc:
                self.stop_event.set()
                break
            try:
                account = ServiceBot.generateAccount()
                self.insert_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Khởi tạo thông tin thành công",
                )
                count_proxy = 1
                while count_proxy <= 20:
                    service_proxy = config.global_config.methodProxy
                    if count_proxy == 20:
                        break
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Đang chờ lấy proxy {service_proxy} {count_proxy} / 20",
                        RUN,
                    )
                    by_proxy = ServiceBot.generateProxy()
                    if by_proxy:
                        account.proxy = by_proxy
                        break
                    time.sleep(5)
                    count_proxy += 1
                if account.proxy is None:
                    totail_error += 1
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Yêu cầu kiểm tra lại proxy",
                        ERROR,
                    )
                    continue
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Khởi tạo trình duyệt proxy {account.proxy}",
                    RUN,
                )
                options = Options()
                options.add_argument("--proxy-server=%s" % account.proxy)
                options.add_argument("--app=http://www.google.com")
                options.add_argument("--disable-blink-features=AutomationControlled")
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                options.add_experimental_option(
                    "excludeSwitches", ["enable-automation"]
                )
                options.add_experimental_option("useAutomationExtension", False)
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
                user_agent = ServiceBot.getRandomeUserAgent()
                if user_agent is None:
                    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
                options.add_argument(f"user-agent={user_agent}")
                print(f"user_agent->{user_agent}")
                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()), options=options
                )
                driver.execute_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                )
                num_columns = int(config.global_config.numberCol)
                row = int(index) // num_columns
                col = int(index) % num_columns
                zx = col * 400
                zy = row * 600
                driver.set_window_rect(zx, zy, 800, 600)
                WAIT = random.randint(15, 30)
                DELAY = random.randint(10, 30) / 10.0
                ########
                driver.get("https://bot.sannysoft.com/")
                ##########
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//a[contains(text(),'Gmail')]")
                    )
                ).click()
                time.sleep(DELAY)
                try:
                    WebDriverWait(driver, WAIT / 2).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//a[contains(text(),'Đăng nhập')]")
                        )
                    ).click()
                except Exception as e:
                    pass
                time.sleep(DELAY)
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//span[contains(text(),'Loại bỏ')]")
                        )
                    ).click()
                except Exception as e:
                    pass
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
                        )
                    )
                ).click()
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//span[contains(text(),'Dành cho mục đích cá nhân của tôi')]",
                        )
                    )
                ).click()
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Nhập họ: {account.firstName} và tên {account.lastName}",
                    RUN,
                )
                time.sleep(DELAY)
                element_lastName = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@name='lastName']"))
                )
                for char in account.lastName:
                    element_lastName.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_lastName.send_keys(Keys.ENTER)
                element_firstName = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@name='firstName']"))
                )
                for char in account.firstName:
                    element_firstName.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_firstName.send_keys(Keys.ENTER)
                gender_string = "nữ"
                if account.gender == 2:
                    gender_string = "nam"
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Nhập ngày sinh: {account.birthDay} và giới tính {gender_string}",
                    RUN,
                )
                time.sleep(DELAY)
                element_day = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="day"]'))
                )
                element_day.click()
                for char in account.birthDay.split("/")[0]:
                    element_day.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                time.sleep(DELAY)
                element_month = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, '//select[@id="month"]'))
                )
                element_month.click()
                for _ in range(1, int(account.birthDay.split("/")[1]) + 1):
                    element_month.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.1 + 0.1 * random.random())
                element_month.send_keys(Keys.ENTER)
                time.sleep(DELAY)
                element_year = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="year"]'))
                )
                element_year.click()
                for char in account.birthDay.split("/")[2]:
                    element_year.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                time.sleep(DELAY)
                element_gender = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, '//select[@id="gender"]'))
                )
                element_gender.click()
                for _ in range(1, account.gender + 1):
                    element_gender.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.1 + 0.1 * random.random())
                element_gender.send_keys(Keys.ENTER)
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
                        )
                    )
                ).click()
                time.sleep(DELAY)
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//button[contains(text(),'Thay vào đó hãy lấy địa chỉ Gmail')]",
                            )
                        )
                    ).click()
                except:
                    pass
                time.sleep(DELAY)
                try:
                    WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[contains(text(),'Tạo địa chỉ Gmail của riêng bạn')]",
                            )
                        )
                    ).click()
                except:
                    pass
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Nhập tên người dùng: {account.username}",
                    RUN,
                )
                time.sleep(DELAY)
                element_username = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@name='Username']"))
                )
                element_username.click()
                for char in account.username:
                    element_username.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_username.send_keys(Keys.ENTER)
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Nhập mật khẩu: {account.password}",
                    RUN,
                )
                time.sleep(DELAY)
                element_passwd = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@name='Passwd']"))
                )
                for char in account.password:
                    element_passwd.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_passwd.send_keys(Keys.ENTER)
                time.sleep(DELAY)
                element_passwd_again = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@name='PasswdAgain']")
                    )
                )
                for char in account.password:
                    element_passwd_again.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_passwd_again.send_keys(Keys.ENTER)
                try:
                    check_error = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[contains(text(),'Rất tiếc, chúng tôi không thể tạo Tài khoản Google cho bạn.')]",
                            )
                        )
                    )
                    if check_error:
                        driver.quit()
                        totail_error += 1
                        self.update_account_event(
                            f"{account.username}@gmail.com",
                            account.password,
                            f"Luồng {index}: Tạo tài khoản thất bại",
                            ERROR,
                        )
                        self.update_error_event(totail_error)
                        self.update_success_event(totail_success)
                        continue
                except:
                    pass
                time.sleep(DELAY)
                check_phone = 1
                while check_phone <= 5:
                    if check_phone == 5:
                        account.phone = None
                        account.idPhone = None
                        break
                    count_phone = 1
                    while count_phone <= 20:
                        service_otp = config.global_config.methodOtp
                        if count_phone == 20:
                            break
                        self.update_account_event(
                            f"{account.username}@gmail.com",
                            account.password,
                            f"Luồng {index}: Đang chờ lấy sim {service_otp} {count_phone} / 20",
                            RUN,
                        )
                        phone, id_phone = ServiceBot.generatePhone()
                        if phone and id_phone:
                            account.phone = phone
                            account.idPhone = id_phone
                            break
                        time.sleep(5)
                        count_phone += 1
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Nhập số điện thoại: {account.phone} và kiểm tra {check_phone} / 4",
                        RUN,
                    )
                    element_phone = WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//*[@id='phoneNumberId']")
                        )
                    )
                    text_length = len(element_phone.get_attribute("value"))
                    if text_length > 0:
                        for _ in range(text_length):
                            element_phone.send_keys(Keys.ARROW_LEFT)
                            time.sleep(0.1 + 0.1 * random.random())
                            element_phone.send_keys(Keys.DELETE)
                    for char in account.phone:
                        element_phone.send_keys(char)
                        time.sleep(0.1 + 0.1 * random.random())
                    element_phone.send_keys(Keys.ENTER)
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//input[@name="code"]')
                            )
                        )
                        break
                    except:
                        account.phone = None
                        account.idPhone = None
                    check_phone += 1
                if account.phone is None or account.idPhone is None:
                    driver.quit()
                    totail_error += 1
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Yêu cầu kiểm tra lại dịch vụ sim",
                        ERROR,
                    )
                    self.update_error_event(totail_error)
                    self.update_success_event(totail_success)
                    continue
                time.sleep(DELAY)
                code = None
                count_code = 1
                while count_code <= 16:
                    if count_code == 16:
                        break
                    service_otp = config.global_config.methodOtp
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Đang chờ lấy code sim {service_otp} {count_code} / 15",
                        RUN,
                    )
                    by_code = ServiceBot.generateCode(account.idPhone)
                    if by_code:
                        code = by_code
                        break
                    time.sleep(5)
                    count_code += 1
                if code is None:
                    driver.quit()
                    totail_error += 1
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Số điện thoại không có otp",
                        ERROR,
                    )
                    self.update_error_event(totail_error)
                    self.update_success_event(totail_success)
                    continue
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Nhập mã code: {code}",
                    RUN,
                )
                element_code = WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="code"]'))
                )
                for char in code:
                    element_code.send_keys(char)
                    time.sleep(0.1 + 0.1 * random.random())
                element_code.send_keys(Keys.ENTER)
                if account.recoveryEmail is None:
                    try:
                        WebDriverWait(driver, WAIT).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//span[contains(text(),'Bỏ qua')]")
                            )
                        ).click()
                        time.sleep(DELAY)
                    except:
                        pass
                else:
                    try:
                        time.sleep(DELAY)
                        element_recovery = (
                            WebDriverWait(driver, WAIT)
                            .until(
                                EC.presence_of_element_located(
                                    (By.XPATH, '//input[@name="recovery"]')
                                )
                            )
                            .send_keys(account.recoveryEmail)
                        )
                        for char in account.recoveryEmail:
                            element_recovery.send_keys(char)
                            time.sleep(0.1 + 0.1 * random.random())
                        time.sleep(DELAY)
                        WebDriverWait(driver, WAIT).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//span[contains(text(),'Tiếp theo')]")
                            )
                        ).click()
                    except:
                        try:
                            WebDriverWait(driver, WAIT).until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//span[contains(text(),'Bỏ qua')]")
                                )
                            ).click()
                            time.sleep(DELAY)
                        except:
                            pass
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
                        )
                    )
                ).click()
                time.sleep(DELAY)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(DELAY)
                WebDriverWait(driver, WAIT).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
                        )
                    )
                ).click()
                ServiceBot.saveDataTXT(account)
                totail_success += 1
                time.sleep(DELAY)
                check_title = 1
                while check_title < 30:
                    title = driver.title
                    if (
                        title == f"Hộp thư đến - {account.username}@gmail.com - Gmail"
                        or title
                        == f"Hộp thư đến (1) - {account.username}@gmail.com - Gmail"
                    ):
                        break
                    check_title += 1
                    time.sleep(2)
                ####### Bật POP/IMAP
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Đang bật POP/IMAP",
                    RUN,
                )
                check_imap = True
                try:
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@aria-label='Trình đơn chính']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@data-tooltip='Cài đặt']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//button[contains(text(),'Xem tất cả chế độ cài đặt')]",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//a[contains(text(),'Chuyển tiếp và POP/IMAP')]",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//input[@type='radio' and @name='bx_pe' and @value='3']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//input[@type='radio' and @name='bx_ie' and @value='1']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    driver.set_window_size(800, 1200)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@class='nH Tv1JD']//button[@guidedhelpid='save_changes_button']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    driver.set_window_size(800, 600)
                except:
                    check_imap = False
                    pass
                if check_imap:
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}:Bật POP/IMAP thành công",
                        RUN,
                    )
                    account.imap = "Đã bật"
                else:
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}:Bật POP/IMAP thất bại",
                        ERROR,
                    )
                    account.imap = "Chưa bật"
                check_title = 1
                while check_title < 30:
                    title = driver.title
                    if (
                        title == f"Hộp thư đến - {account.username}@gmail.com - Gmail"
                        or title
                        == f"Hộp thư đến (1) - {account.username}@gmail.com - Gmail"
                    ):
                        break
                    check_title += 1
                    time.sleep(2)
                ####### Đọc chat ban đầu
                try:
                    time.sleep(DELAY)
                    driver.set_window_size(800, 800)
                    time.sleep(DELAY)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//span[@email='googlecommunityteam-noreply@google.com']",
                            )
                        )
                    ).click()
                    time.sleep(random.randint(30, 80) / 10.0)
                    WebDriverWait(driver, WAIT).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                "//div[@class='ar6 T-I-J3 J-J5-Ji']",
                            )
                        )
                    ).click()
                    time.sleep(DELAY)
                    driver.set_window_size(800, 600)
                except:
                    time.sleep(DELAY)
                    driver.set_window_size(800, 600)
                ####### Gửi thư ngẫu nhiên
                # try:
                #     time.sleep(DELAY)
                #     WebDriverWait(driver, WAIT).until(
                #         EC.presence_of_element_located(
                #             (
                #                 By.XPATH,
                #                 "//div[@class='T-I T-I-KE L3']",
                #             )
                #         )
                #     ).click()
                #     to_email = "vodai109@gmail.com"
                #     subject_email = "Đây là tiêu đề email"
                #     content = "Đây là nội dung email"
                #     time.sleep(DELAY)
                #     element_to = WebDriverWait(driver, WAIT).until(
                #         EC.presence_of_element_located(
                #             (
                #                 By.XPATH,
                #                 "//div[@class='nH Hd']//span[@email='googlecommunityteam-noreply@google.com']",
                #             )
                #         )
                #     )
                ## <input id=":10q" class="agP aFw" peoplekit-id="BbVjBd" autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false" aria-label="Tới người nhận" aria-autocomplete="list" aria-haspopup="listbox" aria-expanded="false" placeholder="" size="0" type="text" role="combobox" aria-owns=":10r" aria-controls=":10r">
                ## <input name="subjectbox" id=":x4" class="aoT" autocomplete="off" spellcheck="true" tabindex="1" placeholder="Tiêu đề" aria-label="Tiêu đề">
                ## <div id=":ye" class="Am aiL Al editable LW-avf tS-tW" hidefocus="true" aria-label="Nội dung thư" g_editable="true" role="textbox" aria-multiline="true" contenteditable="true" tabindex="1" style="direction: ltr; min-height: 256px;" spellcheck="false" aria-owns=":10s" aria-controls=":10s" aria-expanded="false"><br></div>
                ## <div id=":kj" class="T-I J-J5-Ji aoO v7 T-I-atl L3" role="button" tabindex="1" data-tooltip="Gửi &#x202A;(Ctrl-Enter)&#x202C;" aria-label="Gửi &#x202A;(Ctrl-Enter)&#x202C;" data-tooltip-delay="800" jslog="32601; u014N:xr6bB,cOuCgd,Kr2w4b; dYFj7e:true; 11:WyIjbXNnLWE6cjcyNjQxMzEzMjczNjc2NjcyMTIiLG51bGwsbnVsbCxudWxsLDEsbnVsbCxbIiN0aHJlYWQtYTpyLTEwNTU4MDkwMjExOTMyMDU3NTYiXSwwLG51bGwsbnVsbCwwLG51bGwsbnVsbCwwXQ..; 4:W251bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsMCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCwwXQ.." style="user-select: none;">Gửi</div>
                # except:
                #     traceback.print_exc()
                #     pass
                self.update_account_event(
                    f"{account.username}@gmail.com",
                    account.password,
                    f"Luồng {index}: Đã tạo tài khoản thành công",
                    SUCCESS,
                )
                ServiceBot.saveDataCSV(account)
                time.sleep(10)
            except Exception as e:
                traceback.print_exc()
                if driver is not None:
                    driver.quit()
                totail_error += 1
                if account is not None:
                    self.update_account_event(
                        f"{account.username}@gmail.com",
                        account.password,
                        f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
                        ERROR,
                    )
            self.update_error_event(totail_error)
            self.update_success_event(totail_success)
            number_acc = int(config.global_config.numberAccount)
            if totail_success >= number_acc:
                self.stop_event.set()
                break
