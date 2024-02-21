import requests
import json
import time
from models.model import Hcotp


def buy_phone_number(key):
    hcotp = None
    try:
        if key is None:
            return None
        url = "https://hcotp.com/api/v2/createrequest?token={}&serviceId=2&carrier=all".format(
            key
        )
        response = requests.request("GET", url)
        time.sleep(1)
        result = json.loads(response.text)
        print(result)
        if result:
            if result["status"] == 0:
                hcotp = Hcotp(result)
        return hcotp
    except Exception as e:
        return None


def get_otp(key, id_phone):
    hcotp = None
    try:
        url = "https://hcotp.com/api/v2/getcode?token={}&requestId={}".format(
            key, id_phone
        )
        response = requests.request("GET", url)
        time.sleep(1)
        result = json.loads(response.text)
        if result:
            if result["code"]:
                hcotp = Hcotp(result)
        return hcotp
    except Exception as e:
        return None
