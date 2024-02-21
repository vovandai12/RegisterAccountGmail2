import requests
import json
import time
from models.model import Ironsim


def buy_phone_number(key, service):
    ironsim = None
    try:
        if key is None:
            return None
        url = "https://ironsim.com/api/phone/new-session?token={}&service={}".format(
            key, service
        )
        response = requests.request("GET", url)
        time.sleep(1)
        result = json.loads(response.text)
        if result:
            if result["status_code"] == 200:
                ironsim = Ironsim(result["data"])
        return ironsim
    except Exception as e:
        return None


def get_otp(key, id_phone):
    ironsim = None
    try:
        url = "https://ironsim.com/api/session/{}/get-otp?token={}".format(
            id_phone, key
        )
        response = requests.request("GET", url)
        time.sleep(1)
        result = json.loads(response.text)
        print(result)
        if result:
            if result["status_code"] == 200:
                ironsim = Ironsim(result["data"])
        return ironsim
    except Exception as e:
        return None
