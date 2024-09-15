import requests
import json
import time
from models.model import BossOtp
import json


def buy_phone_number(key):
    bossOtp = None
    try:
        if key is None:
            return None
        url = f"https://bossotp.net/api/v4/rents/create?service_id=66272016e137e531866e2cd4&api_token={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if result:
            if "number" in result:
                bossOtp = BossOtp(result)
        return bossOtp
    except Exception as e:
        return None


def get_otp(key, rent_id):
    bossOtp = None
    try:
        url = f"https://bossotp.net/api/v4/rents/check?_id={rent_id}&api_token={key}"
        response = requests.request("GET", url)
        result = json.loads(response.text)
        print(result)
        if result:
            if result["status"] == "SUCCESS":
                bossOtp = BossOtp(result)
        return bossOtp
    except Exception as e:
        return None
