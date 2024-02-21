import os
from datetime import datetime
import string
import random
import csv
import unidecode
import config as config
from file_paths import FilePaths
from models.model import Account
from config import (
    TMPROXY,
    PROXYSHOPLIKE,
    PROXYFB,
    BOSSOTP,
    IRONSIM,
    VIOTP,
    SIMOTP,
    HCOTP,
)
import bot.tmproxy as Tmproxy
import bot.proxyshoplike as Proxyshoplike
import bot.proxyfb as Proxyfb
import bot.ironsim as Ironsim
import bot.bossotp as Bossotp
import bot.viotp as Viotp
import bot.simotp as Simotp
import bot.hcotp as Hcotp
import re


def generateAccount():
    try:
        first_name, last_name = generateFullName()
        account = Account()
        account.firstName = first_name
        account.lastName = last_name
        account.username = generateUsername(first_name, last_name)
        account.password = generatePassword()
        account.recoveryEmail = generateRecoveryEmail()
        account.birthDay = generateBirthday()
        account.gender = generateGender()
        return account
    except Exception as e:
        return None


def generatePassword():
    try:
        if config.global_config.randomPassword == "agree":
            chars = (
                string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits
                + string.punctuation
            )
            size = random.randint(10, 20)
            return "".join(random.choice(chars) for x in range(size))
        else:
            return config.global_config.defaultPassword
    except Exception as e:
        return None


def generateFullName():
    try:
        first_name_file = None
        last_name_file = None
        if config.global_config.fullName == "VN":
            first_name_file = open(FilePaths.FIRST_NAME_VN.value, "r", encoding="utf-8")
            last_name_file = open(FilePaths.LAST_NAME_VN.value, "r", encoding="utf-8")
        elif config.global_config.fullName == "US":
            first_name_file = open(FilePaths.FIRST_NAME_US.value, "r", encoding="utf-8")
            last_name_file = open(FilePaths.LAST_NAME_US.value, "r", encoding="utf-8")
        first_names = csv.reader(first_name_file)
        first_names = list(first_names)
        first_name = random.choice(first_names)[0]
        last_names = csv.reader(last_name_file)
        last_names = list(last_names)
        last_name = random.choice(last_names)[0]
        return first_name, last_name
    except Exception as e:
        return None, None


def generateBirthday():
    try:
        birthday = (
            str(random.randint(1, 28))
            + "/"
            + str(random.randint(1, 12))
            + "/"
            + str(random.randint(1980, 2004))
        )
        return birthday
    except Exception as e:
        return None


def generateGender():
    try:
        gender = None
        if config.global_config.gender == "random":
            gender = random.randint(1, 2)
        elif config.global_config.gender == "male":
            gender = 2
        elif config.global_config.gender == "female":
            gender = 1
        return gender
    except Exception as e:
        return None


def generateUsername(first_name, last_name):
    try:
        firstName = unidecode.unidecode(first_name).lower()
        lastName = unidecode.unidecode(last_name).lower()
        rand_5_digit_num = random.randint(10000, 9999999)
        user_name = firstName + "." + lastName
        random_username = random.randint(0, 2)
        if random_username == 0:
            user_name = firstName + lastName
        if random_username == 1:
            user_name = firstName + "." + lastName + "."
        user_name = user_name.lower() + str(rand_5_digit_num)
        return user_name.replace(" ", ".")
    except Exception as e:
        return None


def generateRecoveryEmail():
    try:
        path = config.global_config.fileRecovery
        if path:
            with open(path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    random_line = random.choice(lines)
                    recovery = random_line.strip()
                    return recovery
                else:
                    return None
        return None
    except Exception as e:
        return None


def generateProxy():
    try:
        proxy = None
        key = config.global_config.keyProxy
        value = config.global_config.methodProxy
        if key:
            for item in key:
                if value == TMPROXY:
                    by_proxy = Tmproxy.get_proxy(item)
                    if by_proxy:
                        proxy = by_proxy.https
                        break
                elif value == PROXYSHOPLIKE:
                    by_proxy = Proxyshoplike.get_proxy(item)
                    if by_proxy:
                        proxy = by_proxy.proxy
                        break
                elif value == PROXYFB:
                    by_proxy = Proxyfb.get_proxy(item)
                    if by_proxy:
                        proxy = by_proxy.proxy
                        break
            if proxy is not None:
                return proxy
        return proxy
    except Exception as e:
        return None


def generatePhone():
    try:
        phone = None
        id_phone = None
        value = config.global_config.methodOtp
        key = config.global_config.keyOtp
        if key:
            if value == BOSSOTP:
                buy_phone = Bossotp.buy_phone_number(key)
                if buy_phone:
                    id_phone = buy_phone.rent_id
                    numeric_str = "".join(filter(str.isdigit, buy_phone.number))
                    result_str = "0" + numeric_str[1:]
                    phone = result_str
            elif value == IRONSIM:
                buy_phone = Ironsim.buy_phone_number(key, 16)
                if buy_phone:
                    phone = "0" + buy_phone.phone_number
                    id_phone = buy_phone.session
            elif value == VIOTP:
                buy_phone = Viotp.buy_phone_number(key)
                if buy_phone:
                    phone = "0" + buy_phone.phone_number
                    id_phone = buy_phone.request_id
            elif value == SIMOTP:
                buy_phone = Simotp.buy_phone_number(key, 49)
                if buy_phone:
                    phone = "0" + buy_phone.phoneNumber
                    id_phone = buy_phone.id
            elif value == HCOTP:
                buy_phone = Hcotp.buy_phone_number(key)
                if buy_phone:
                    phone = buy_phone.phoneNum
                    id_phone = buy_phone.id
        return phone, id_phone
    except Exception as e:
        return None, None


def generateCode(id_phone):
    try:
        code = None
        value = config.global_config.methodOtp
        key = config.global_config.keyOtp
        if key:
            if value == BOSSOTP:
                buy_phone = Bossotp.get_otp(key, id_phone)
                if buy_phone:
                    sms_content = buy_phone.sms_content
                    if sms_content:
                        otp_pattern = r"\d+"
                        otp_matches = re.findall(otp_pattern, sms_content)
                        code = otp_matches[0]
            elif value == IRONSIM:
                buy_phone = Ironsim.get_otp(key, id_phone)
                if buy_phone:
                    if buy_phone.messages:
                        code = buy_phone.messages[0]["otp"]
            elif value == VIOTP:
                buy_phone = Viotp.get_otp(key, id_phone)
                if buy_phone:
                    code = buy_phone.Code
            elif value == SIMOTP:
                buy_phone = Simotp.get_otp(key, id_phone)
                if buy_phone:
                    sms_content = buy_phone.content
                    if sms_content:
                        match = re.search(r"(?<!\d)\d+(?!\d)", sms_content)
                        if match:
                            code = match.group()
            elif value == HCOTP:
                hcotp = Hcotp.get_otp(key, id_phone)
                if hcotp:
                    if hcotp.code:
                        code = hcotp.code
        return code
    except Exception as e:
        return None


def saveDataCSV(account):
    service_otp = config.global_config.methodOtp
    service_proxy = config.global_config.methodProxy
    count = 1
    while count <= 20:
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_name = (
                f"{FilePaths.ACCOUNTS_CSV.value}account-{current_date}-{count}.csv"
            )
            if not os.path.isfile(file_name):
                with open(file_name, "w", newline="", encoding="utf-8") as file_csv:
                    writer = csv.writer(file_csv)
                    writer.writerow(
                        [
                            "Gmail",
                            "Password",
                            "RecoveryEmail",
                            "FullName",
                            "BirthDay",
                            "Gender",
                            "ServicePhone",
                            "Phone",
                            "ServiceProxy",
                            "Proxy",
                            "CreateDate",
                        ]
                    )
                    writer.writerow(
                        [
                            f"{account.username}@gmail.com",
                            f"{account.password}",
                            f"{account.recoveryEmail}",
                            f"{account.firstName} {account.lastName}",
                            f"{account.birthDay}",
                            f"{account.gender}",
                            f"{service_otp}",
                            f"{account.phone}",
                            f"{service_proxy}",
                            f"{account.proxy}",
                            f"{account.createDate}",
                        ]
                    )
                return
            with open(file_name, "a", newline="", encoding="utf-8") as file_csv:
                writer = csv.writer(file_csv)
                writer.writerow(
                    [
                        f"{account.username}@gmail.com",
                        f"{account.password}",
                        f"{account.recoveryEmail}",
                        f"{account.firstName} {account.lastName}",
                        f"{account.birthDay}",
                        f"{account.gender}",
                        f"{service_otp}",
                        f"{account.phone}",
                        f"{service_proxy}",
                        f"{account.proxy}",
                        f"{account.createDate}",
                    ]
                )
            return
        except Exception as e:
            count += 1


def saveDataTXT(account):
    count = 1
    while count <= 20:
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            file_name = (
                f"{FilePaths.ACCOUNTS_TXT.value}\\account-{current_date}-{count}.txt"
            )
            if not os.path.isfile(file_name):
                new_data = f"{account.username}@gmail.com|{account.password}|{account.recoveryEmail} \n"
                with open(
                    file_name,
                    "w",
                    encoding="utf-8",
                ) as file:
                    file.write(new_data)
                return
            with open(file_name, "r", encoding="utf-8") as file:
                existing_data = file.read()
            new_data = f"{account.username}@gmail.com|{account.password}|{account.recoveryEmail} \n"
            combined_data = existing_data + new_data
            with open(
                file_name,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(combined_data)
            return
        except Exception as e:
            count += 1


def getRandomeUserAgent():
    try:
        with open(FilePaths.USERAGENT.value, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                random_line = random.choice(lines)
                useragent = random_line.strip()
                return useragent
            else:
                return None
    except Exception as e:
        return None
