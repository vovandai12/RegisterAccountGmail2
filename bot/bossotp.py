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
        url = "https://bossotp.com/api/v1/rent"
        payload = json.dumps({"service_id": "62f615ec1b953f97d5a69c8f"})
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep(1)
        result = json.loads(response.text)
        if result:
            rent_id = result["rent_id"]
            if rent_id:
                i = 0
                while i < 5:
                    i = i + 1
                    time.sleep(5)
                    urlRent = "https://bossotp.com/api/v1/rent/{}".format(rent_id)
                    headersRent = {"Authorization": f"Bearer {key}"}
                    response = requests.request("GET", urlRent, headers=headersRent)
                    result = json.loads(response.text)
                    print(result)
                    if result["status_description"] == "GET_NUMBER_SUCCESS":
                        bossOtp = BossOtp(result)
                        return bossOtp
        return bossOtp
    except Exception as e:
        return None


def get_otp(key, rent_id):
    bossOtp = None
    try:
        headers = {"Authorization": f"Bearer {key}"}
        url = "https://bossotp.com/api/v1/rent/{}".format(rent_id)
        response = requests.request("GET", url, headers=headers)
        time.sleep(1)
        result = json.loads(response.text)
        if result["status_description"] == "GET_SMS_SUCCESS":
            bossOtp = BossOtp(result)
            return bossOtp
    except Exception as e:
        return None
