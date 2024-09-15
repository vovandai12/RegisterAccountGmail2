# options = Options()
# options.add_argument("--proxy-server=%s" % account.proxy)
# options.add_argument("--app=http://www.google.com")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-web-security")
# options.add_argument("--allow-running-insecure-content")
# options.add_experimental_option(
#     "excludeSwitches", ["enable-automation"]
# )
# options.add_experimental_option("useAutomationExtension", False)
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--no-sandbox")
# options.add_argument("disable-popup-blocking")
# options.add_argument("disable-notifications")
# options.add_argument("disable-popup-blocking")
# options.add_argument("--ignore-ssl-errors=yes")
# options.add_argument("--ignore-certificate-errors")
# prefs = {
#     "profile.password_manager_enabled": False,
#     "credentials_enable_service": False,
#     "useAutomationExtension": False,
#     "profile.default_content_setting_values.geolocation": 1,
# }
# options.add_experimental_option("prefs", prefs)
# user_agent = ServiceBot.getRandomeUserAgent()
# if user_agent is None:
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
# # user_agent = UserAgent().random
# options.add_argument(f"user-agent={user_agent}")
# options.add_experimental_option(
#     "prefs", {"profile.default_content_setting_values.geolocation": 1}
# )
# print(f"user_agent->{user_agent}")
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()), options=options
# )
# stealth(
#     driver,
#     user_agent=user_agent,
#     languages=["vi-VN", "vi", "fr-FR", "fr", "en-US", "en"],
#     vendor="Google Inc.",
#     platform="Win32",
#     webgl_vendor="Intel Inc.",
#     renderer="Intel Iris OpenGL Engine",
#     fix_hairline=True,
# )
# driver.execute_script(
#     "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
# )
########
# driver.get("https://infosimples.github.io/detect-headless/")
# driver.get("https://bot.sannysoft.com/")
# driver.get("https://iphey.com/")
##########
# time.sleep(DELAY)
# WebDriverWait(driver, WAIT).until(
#     EC.presence_of_element_located(
#         (By.XPATH, "//a[contains(text(),'Gmail')]")
#     )
# ).click()
# time.sleep(DELAY)
# try:
#     WebDriverWait(driver, WAIT / 2).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//a[contains(text(),'Đăng nhập')]")
#         )
#     ).click()
# except Exception as e:
#     pass
# time.sleep(DELAY)
# try:
#     WebDriverWait(driver, 5).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//span[contains(text(),'Loại bỏ')]")
#         )
#     ).click()
# except Exception as e:
#     pass
# time.sleep(DELAY)
# WebDriverWait(driver, WAIT).until(
#     EC.presence_of_element_located(
#         (
#             By.XPATH,
#             "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
#         )
#     )
# ).click()
# time.sleep(DELAY)


####### Bật POP/IMAP
# self.update_account_event(
#     f"{account.username}@gmail.com",
#     account.password,
#     f"Luồng {index}: Đang bật POP/IMAP",
#     RUN,
# )
# check_imap = True
# try:
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//div[@aria-label='Trình đơn chính']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//div[@data-tooltip='Cài đặt']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//button[contains(text(),'Xem tất cả chế độ cài đặt')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//a[contains(text(),'Chuyển tiếp và POP/IMAP')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//input[@type='radio' and @name='bx_pe' and @value='3']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     driver.set_window_size(800, 1200)
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//input[@type='radio' and @name='bx_ie' and @value='1']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//div[@class='nH Tv1JD']//button[@guidedhelpid='save_changes_button']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     driver.set_window_size(800, 600)
# except:
#     check_imap = False
#     pass

# if check_imap:
#     self.update_account_event(
#         f"{account.username}@gmail.com",
#         account.password,
#         f"Luồng {index}:Bật POP/IMAP thành công",
#         RUN,
#     )
#     account.imap = "Đã bật"
# else:
#     self.update_account_event(
#         f"{account.username}@gmail.com",
#         account.password,
#         f"Luồng {index}:Bật POP/IMAP thất bại",
#         ERROR,
#     )
#     account.imap = "Chưa bật"
# check_title = 1
# while check_title < 30:
#     title = driver.title
#     if (
#         title == f"Hộp thư đến - {account.username}@gmail.com - Gmail"
#         or title
#         == f"Hộp thư đến (1) - {account.username}@gmail.com - Gmail"
#         or title == f"Inbox (1) - {account.username}@gmail.com - Gmail"
#         or title == f"Inbox - {account.username}@gmail.com - Gmail"
#     ):
#         break
#     check_title += 1
#     time.sleep(2)
####### Cấu hình chung
# try:
#     driver.get(f"https://myaccount.google.com/security")
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//div[contains(text(),'Bảo vệ tài khoản của bạn')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     driver.execute_script(
#         "window.scrollTo(0, document.body.scrollHeight)"
#     )
#     time.sleep(DELAY)
#     elements = WebDriverWait(driver, WAIT).until(
#         EC.presence_of_all_elements_located(
#             (
#                 By.XPATH,
#                 "//div[@class='HLEawd VfPpkd-ksKsZd-XxIAqe']",
#             )
#         )
#     )
#     for element in elements:
#         if "Duyệt web an toàn" in element.text:
#             element.click()
#             break
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//span[contains(text(),'Tiếp tục')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//span[contains(text(),'Bật')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     for element in elements:
#         if "Đăng nhập và khôi phục" in element.text:
#             element.click()
#             break
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//button[@aria-label='Thêm email khôi phục']",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     element_password = WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//input[@type='password']")
#         )
#     )
#     for char in account.password:
#         element_password.send_keys(char)
#         time.sleep(0.1 + 0.1 * random.random())
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//span[contains(text(),'Tiếp theo')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     element_email = WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (By.XPATH, "//input[@type='email']")
#         )
#     )
#     for char in account.recoveryEmail:
#         element_email.send_keys(char)
#         time.sleep(0.1 + 0.1 * random.random())
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//span[contains(text(),'Tiếp theo')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//a[contains(text(),'Xác minh sau')]",
#             )
#         )
#     ).click()
#     time.sleep(DELAY)
#     WebDriverWait(driver, WAIT).until(
#         EC.presence_of_element_located(
#             (
#                 By.XPATH,
#                 "//span[contains(text(),'Xong')]",
#             )
#         )
#     ).click()
# except:
#     traceback.print_exc()
#     pass
