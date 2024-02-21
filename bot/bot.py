# from threading import Thread, Event
# from datetime import datetime
# import traceback
# import logging
# import utils.config as config
# from utils.config import SUCCESS, ERROR, RUN
# import time
# import random
# import services.service as Service
# from utils.file_paths import FilePaths
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service as ServiceChrome
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from gologin import GoLogin
# from gologin import getRandomPort

# logger = logging.getLogger("Register-Account-Gmail")

# totail_error = 0
# totail_success = 0


# class Bot:
#     def __init__(self, config={}):
#         self.insert_account_event = lambda v: v
#         self.update_account_event = lambda v: v
#         self.add_log_event = lambda v: v
#         self.update_error_event = lambda v: v
#         self.update_success_event = lambda v: v
#         self.stop_event = Event()
#         self.text = {"title": "", "text_list": []}

#     def Stop(self):
#         try:
#             self.stop_event.set()
#         except Exception as e:
#             traceback.print_exc()
#             logger.exception("Exception Stop")

#     def Start(self):
#         try:
#             global totail_error
#             totail_error = 0
#             global totail_success
#             totail_success = 0
#             self.update_error_event(totail_error)
#             self.update_success_event(totail_success)
#             number_thread = int(config.global_config.numberThread)
#             for index in range(0, number_thread):
#                 self.AddLog(status=RUN, append=f"Luồng {index}: Bắt đầu thực thi")
#                 thread = Thread(target=self.DoWorker, args=(index,))
#                 # thread = Thread(target=self.DemoWorker, args=(index,))
#                 thread.daemon = True
#                 thread.start()
#             print("main done")
#         except Exception as e:
#             traceback.print_exc()
#             logger.exception(f"Exception Start")

#     def DoWorker(self, index):
#         global totail_error
#         global totail_success
#         count_event = 0
#         while not self.stop_event.is_set():
#             count_event += 1
#             driver = None
#             gologin = None
#             profile_id = None
#             account = None
#             self.update_error_event(totail_error)
#             self.update_success_event(totail_success)
#             number_acc = int(config.global_config.numberAccount)
#             if totail_success >= number_acc:
#                 self.stop_event.set()
#                 break
#             try:
#                 self.AddLog(
#                     status=SUCCESS, append=f"Luồng {index}: Thực thi lần {count_event}"
#                 )
#                 account = Service.generateAccount()
#                 self.AddLog(
#                     status=SUCCESS,
#                     append=f"Luồng {index}: Khởi tạo thông tin thành công",
#                 )
#                 self.insert_account_event(
#                     f"{account.username}@gmail.com",
#                     account.password,
#                     account.recoveryEmail,
#                     account.phone,
#                     f"Luồng {index}: Khởi tạo thông tin thành công",
#                 )
#                 count_proxy = 1
#                 while count_proxy <= 20:
#                     service_proxy = config.global_config.methodProxy
#                     if count_proxy == 20:
#                         break
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Đang chờ lấy proxy {service_proxy} {count_proxy} / 20",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Đang chờ lấy proxy {service_proxy} {count_proxy} / 20",
#                         SUCCESS,
#                     )
#                     by_proxy = Service.generateProxy()
#                     if by_proxy:
#                         account.proxy = by_proxy
#                         break
#                     time.sleep(5)
#                     count_proxy += 1
#                 if account.proxy is None:
#                     totail_error += 1
#                     self.AddLog(
#                         status=ERROR,
#                         append=f"Luồng {index}: Yêu cầu kiểm tra lại proxy",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Yêu cầu kiểm tra lại proxy",
#                         ERROR,
#                     )
#                     continue
#                 # account.proxy = "95.164.207.13:8080:e12582:proxy11"
#                 print(account.proxy)
#                 self.AddLog(
#                     status=SUCCESS,
#                     append=f"Luồng {index}: Khởi tạo trình duyệt proxy {account.proxy}",
#                 )
#                 self.update_account_event(
#                     f"{account.username}@gmail.com",
#                     account.password,
#                     account.recoveryEmail,
#                     account.phone,
#                     f"Luồng {index}: Khởi tạo trình duyệt proxy {account.proxy}",
#                     SUCCESS,
#                 )
#                 profile_id = Service.generateProfileGologin(
#                     token=config.global_config.token,
#                     profile_name=f"profile_{index}",
#                     proxy=account.proxy,
#                 )
#                 if profile_id is not None:
#                     try:
#                         random_port = getRandomPort()
#                         gologin = GoLogin(
#                             {
#                                 "token": config.global_config.token,
#                                 "profile_id": profile_id,
#                                 "port": random_port,
#                             }
#                         )
#                         debugger_address = gologin.start()
#                         chrome_options = Options()
#                         chrome_options.add_experimental_option(
#                             "debuggerAddress", debugger_address
#                         )
#                         driver = webdriver.Chrome(
#                             service=ServiceChrome(
#                                 executable_path=FilePaths.CHROME_DRIVER.value
#                             ),
#                             options=chrome_options,
#                         )
#                         num_columns = int(config.global_config.numberCol)
#                         row = int(index) // num_columns
#                         col = int(index) % num_columns
#                         zx = col * 400
#                         zy = row * 600
#                         driver.set_window_rect(zx, zy, 400, 600)
#                     except:
#                         totail_error += 1
#                         self.AddLog(
#                             status=ERROR,
#                             append=f"Luồng {index}: Không thể thực thi trình duyệt proxy {account.proxy}",
#                         )
#                         self.update_account_event(
#                             f"{account.username}@gmail.com",
#                             account.password,
#                             account.recoveryEmail,
#                             account.phone,
#                             f"Luồng {index}: Không thể thực thi trình duyệt proxy {account.proxy}",
#                             ERROR,
#                         )
#                         continue
#                     WAIT = 20
#                     DELAY = random.randint(2, 5)
#                     driver.get("chrome://version")
#                     time.sleep(DELAY)
#                     driver.get("https://accounts.google.com/")
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//span[contains(text(),'For my personal use')]")
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Nhập họ: {account.firstName} và tên {account.lastName}",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Nhập họ: {account.firstName} và tên {account.lastName}",
#                         SUCCESS,
#                     )
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//*[@name='firstName']")
#                         )
#                     ).send_keys(account.firstName)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//*[@name='lastName']")
#                         )
#                     ).send_keys(account.lastName)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     gender_string = "nam"
#                     if account.gender == 2:
#                         gender_string = "nữ"
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Nhập ngày sinh: {account.birthDay} và giới tính {gender_string}",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Nhập ngày sinh: {account.birthDay} và giới tính {gender_string}",
#                         SUCCESS,
#                     )
#                     select_acc_month = WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, '//select[@id="month"]')
#                         )
#                     )
#                     acc_month = Select(select_acc_month)
#                     acc_month.select_by_value(account.birthDay.split("/")[1])
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, '//input[@name="day"]')
#                         )
#                     ).send_keys(account.birthDay.split("/")[0])
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, '//input[@name="year"]')
#                         )
#                     ).send_keys(account.birthDay.split("/")[2])
#                     time.sleep(DELAY)
#                     select_acc_gender = WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, '//select[@id="gender"]')
#                         )
#                     )
#                     acc_gender = Select(select_acc_gender)
#                     acc_gender.select_by_value(f"{account.gender}")
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     try:
#                         WebDriverWait(driver, 5).until(
#                             EC.presence_of_element_located(
#                                 (
#                                     By.XPATH,
#                                     "//button[contains(text(),'Get a Gmail address instead')]",
#                                 )
#                             )
#                         ).click()
#                         time.sleep(DELAY)
#                     except:
#                         pass
#                     try:
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (
#                                     By.XPATH,
#                                     "//div[contains(text(),'Create your own Gmail address')]",
#                                 )
#                             )
#                         ).click()
#                         time.sleep(DELAY)
#                     except:
#                         pass
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Nhập tên người dùng: {account.username}",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Nhập tên người dùng: {account.username}",
#                         SUCCESS,
#                     )
#                     user_name_tag = WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//*[@name='Username']")
#                         )
#                     )
#                     user_name_tag.clear()
#                     time.sleep(DELAY)
#                     user_name_tag.send_keys(account.username)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Nhập mật khẩu: {account.password}",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Nhập mật khẩu: {account.password}",
#                         SUCCESS,
#                     )
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//*[@name='Passwd']")
#                         )
#                     ).send_keys(account.password)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, "//*[@name='PasswdAgain']")
#                         )
#                     ).send_keys(account.password)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     check_phone = 1
#                     while check_phone <= 5:
#                         if check_phone == 5:
#                             account.phone = None
#                             account.idPhone = None
#                             break
#                         count_phone = 1
#                         while count_phone <= 20:
#                             service_otp = config.global_config.methodOtp
#                             if count_phone == 20:
#                                 break
#                             self.AddLog(
#                                 status=SUCCESS,
#                                 append=f"Luồng {index}: Đang chờ lấy sim {service_otp} {count_phone} / 20",
#                             )
#                             self.update_account_event(
#                                 f"{account.username}@gmail.com",
#                                 account.password,
#                                 account.recoveryEmail,
#                                 account.phone,
#                                 f"Luồng {index}: Đang chờ lấy sim {service_otp} {count_phone} / 20",
#                                 SUCCESS,
#                             )
#                             phone, id_phone = Service.generatePhone()
#                             if phone and id_phone:
#                                 account.phone = phone
#                                 account.idPhone = id_phone
#                                 break
#                             time.sleep(5)
#                             count_phone += 1
#                         self.AddLog(
#                             status=SUCCESS,
#                             append=f"Luồng {index}: Nhập số điện thoại: {account.phone} và kiểm tra {check_phone} / 4",
#                         )
#                         self.update_account_event(
#                             f"{account.username}@gmail.com",
#                             account.password,
#                             account.recoveryEmail,
#                             account.phone,
#                             f"Luồng {index}: Nhập số điện thoại: {account.phone} và kiểm tra {check_phone} / 4",
#                             SUCCESS,
#                         )
#                         tag_phone = WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (By.XPATH, "//*[@id='phoneNumberId']")
#                             )
#                         )
#                         tag_phone.clear()
#                         time.sleep(2)
#                         tag_phone.send_keys(account.phone)
#                         time.sleep(DELAY)
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (
#                                     By.XPATH,
#                                     "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                                 )
#                             )
#                         ).click()
#                         try:
#                             WebDriverWait(driver, 5).until(
#                                 EC.presence_of_element_located(
#                                     (By.XPATH, '//input[@name="code"]')
#                                 )
#                             )
#                             break
#                         except:
#                             account.phone = None
#                             account.idPhone = None
#                         check_phone += 1
#                     if account.phone is None or account.idPhone is None:
#                         driver.quit()
#                         time.sleep(3)
#                         gologin.stop()
#                         gologin.delete(profile_id)
#                         totail_error += 1
#                         self.AddLog(
#                             status=ERROR,
#                             append=f"Luồng {index}: Yêu cầu kiểm tra lại dịch vụ sim",
#                         )
#                         self.update_account_event(
#                             f"{account.username}@gmail.com",
#                             account.password,
#                             account.recoveryEmail,
#                             account.phone,
#                             f"Luồng {index}: Yêu cầu kiểm tra lại dịch vụ sim",
#                             ERROR,
#                         )
#                         continue
#                     code = None
#                     count_code = 1
#                     while count_code <= 16:
#                         if count_code == 16:
#                             break
#                         service_otp = config.global_config.methodOtp
#                         self.AddLog(
#                             status=SUCCESS,
#                             append=f"Luồng {index}: Đang chờ lấy code sim {service_otp} {count_code} / 15",
#                         )
#                         self.update_account_event(
#                             f"{account.username}@gmail.com",
#                             account.password,
#                             account.recoveryEmail,
#                             account.phone,
#                             f"Luồng {index}: Đang chờ lấy code sim {service_otp} {count_code} / 15",
#                             SUCCESS,
#                         )
#                         by_code = Service.generateCode(account.idPhone)
#                         if by_code:
#                             code = by_code
#                             break
#                         time.sleep(5)
#                         count_code += 1
#                     if code is None:
#                         driver.quit()
#                         time.sleep(3)
#                         gologin.stop()
#                         gologin.delete(profile_id)
#                         totail_error += 1
#                         self.AddLog(
#                             status=ERROR,
#                             append=f"Luồng {index}: Yêu cầu kiểm tra lại dịch vụ sim",
#                         )
#                         self.update_account_event(
#                             f"{account.username}@gmail.com",
#                             account.password,
#                             account.recoveryEmail,
#                             account.phone,
#                             f"Luồng {index}: Yêu cầu kiểm tra lại dịch vụ sim",
#                             ERROR,
#                         )
#                         continue
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Nhập mã code: {code}",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Nhập mã code: {code}",
#                         SUCCESS,
#                     )
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (By.XPATH, '//input[@name="code"]')
#                         )
#                     ).send_keys(code)
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     try:
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (By.XPATH, '//input[@name="recovery"]')
#                             )
#                         ).send_keys(account.recoveryEmail)
#                         time.sleep(DELAY)
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (By.XPATH, "//span[contains(text(),'Next')]")
#                             )
#                         ).click()
#                         time.sleep(DELAY)
#                     except:
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (By.XPATH, "//span[contains(text(),'Skip')]")
#                             )
#                         ).click()
#                         time.sleep(DELAY)
#                     try:
#                         WebDriverWait(driver, WAIT).until(
#                             EC.presence_of_element_located(
#                                 (By.XPATH, "//span[contains(text(),'Skip')]")
#                             )
#                         ).click()
#                         time.sleep(DELAY)
#                         print("Đã click skip")
#                     except:
#                         pass
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     time.sleep(DELAY)
#                     driver.execute_script("window.scrollTo(0, 1000)")
#                     time.sleep(DELAY)
#                     WebDriverWait(driver, WAIT).until(
#                         EC.presence_of_element_located(
#                             (
#                                 By.XPATH,
#                                 "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
#                             )
#                         )
#                     ).click()
#                     ##### Lưu dữ liệu
#                     time.sleep(5)
#                     Service.saveDataCSV(account)
#                     Service.saveDataTXT(account)
#                     time.sleep(5)
#                     driver.get("https://mail.google.com")
#                     time.sleep(10)
#                     time.sleep(5)
#                     driver.quit()
#                     time.sleep(3)
#                     gologin.stop()
#                     gologin.delete(profile_id)
#                     totail_success += 1
#                     self.AddLog(
#                         status=RUN,
#                         append=f"Luồng {index}: Đã tạo tài khoản thành công",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Đã tạo tài khoản thành công",
#                         RUN,
#                     )
#                 else:
#                     totail_error += 1
#                     self.AddLog(
#                         status=ERROR,
#                         append=f"Luồng {index}: Tạo tài khoản thất bại: Khởi tạo trình duyệt không thành công",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Tạo tài khoản thất bại: Khởi tạo trình duyệt không thành công",
#                         ERROR,
#                     )
#             except Exception as e:
#                 traceback.print_exc()
#                 logger.exception(f"Exception DoWorker")
#                 if driver is not None:
#                     driver.quit()
#                 time.sleep(3)
#                 if gologin is not None:
#                     gologin.stop()
#                     if profile_id is not None:
#                         gologin.delete(profile_id)
#                 totail_error += 1
#                 self.AddLog(
#                     status=ERROR,
#                     append=f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                 )
#                 self.update_account_event(
#                     f"{account.username}@gmail.com",
#                     account.password,
#                     account.recoveryEmail,
#                     account.phone,
#                     f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                     ERROR,
#                 )
#             self.update_error_event(totail_error)
#             self.update_success_event(totail_success)
#             number_acc = int(config.global_config.numberAccount)
#             if totail_success >= number_acc:
#                 self.stop_event.set()
#                 break
#         self.AddLog(status=RUN, append=f"Luồng {index}: Đã hoàn thành")

#     def AddLog(self, status, **kwargs):
#         try:
#             dt_string = datetime.now().strftime("[%H:%M:%S]")
#             text_list = "text_list"
#             insert = "insert"
#             index = "index"
#             append = "append"
#             self.text[text_list].clear()
#             if insert in kwargs:
#                 self.text[text_list].insert(
#                     kwargs.get(index, 0), dt_string + " " + kwargs[insert].lower()
#                 )
#             if append in kwargs:
#                 self.text[text_list].append(dt_string + " " + kwargs[append].lower())
#             self.add_log_event(self.text, status)
#         except Exception as e:
#             traceback.print_exc()
#             logger.exception(f"Exception AddLog")

#     def DemoWorker(self, index):
#         global totail_error
#         global totail_success
#         count_event = 1
#         while not self.stop_event.is_set():
#             try:
#                 self.AddLog(
#                     status=SUCCESS, append=f"Luồng {index}: Thực thi lần {count_event}"
#                 )
#                 account = Service.generateAccount()
#                 time.sleep(2)
#                 self.AddLog(
#                     status=SUCCESS,
#                     append=f"Luồng {index}: Khởi tạo thông tin thành công",
#                 )
#                 self.insert_account_event(
#                     f"{account.username}@gmail.com",
#                     account.password,
#                     account.recoveryEmail,
#                     account.phone,
#                     f"Luồng {index}: Khởi tạo thông tin thành công",
#                 )
#                 time.sleep(3)
#                 check = random.randint(1, 3)
#                 if check == 1:
#                     totail_error += 1
#                     self.AddLog(
#                         status=ERROR,
#                         append=f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                         ERROR,
#                     )
#                 elif check == 2:
#                     self.AddLog(
#                         status=SUCCESS,
#                         append=f"Luồng {index}: Đang tạo tài khoản",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Đang tạo tài khoản",
#                         SUCCESS,
#                     )
#                 elif check == 3:
#                     totail_success += 1
#                     self.AddLog(
#                         status=RUN,
#                         append=f"Luồng {index}: Đã tạo tài khoản thành công",
#                     )
#                     self.update_account_event(
#                         f"{account.username}@gmail.com",
#                         account.password,
#                         account.recoveryEmail,
#                         account.phone,
#                         f"Luồng {index}: Đã tạo tài khoản thành công",
#                         RUN,
#                     )
#             except Exception as e:
#                 traceback.print_exc()
#                 totail_error += 1
#                 self.AddLog(
#                     status=ERROR,
#                     append=f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                 )
#                 self.update_account_event(
#                     f"{account.username}@gmail.com",
#                     account.password,
#                     account.recoveryEmail,
#                     account.phone,
#                     f"Luồng {index}: Tạo tài khoản thất bại: Lỗi không xác định",
#                     ERROR,
#                 )
#             self.update_error_event(totail_error)
#             self.update_success_event(totail_success)
#             number_acc = int(config.global_config.numberAccount)
#             if totail_success >= number_acc:
#                 self.stop_event.set()
#                 break
#             count_event += 1
#         self.AddLog(status=RUN, append=f"Luồng {index}: Đã hoàn thành")
