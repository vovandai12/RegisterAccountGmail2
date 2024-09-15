from models.model import Chaycodeso3
import requests, json


def buy_phone_number(key):
    try:
        data = None
        if key is not None:
            url = f"https://chaycodeso3.com/api?act=number&apik={key}&appId=1005"
            response = requests.request("GET", url)
            result = json.loads(response.text)
            print(result)
            if result:
                if result["ResponseCode"] == 0:
                    data = Chaycodeso3(result["Result"])
        return data
    except:
        return None


def get_otp(key, id_phone):
    try:
        data = None
        if key is not None:
            url = f"http://chaycodeso3.com/api?act=code&apik={key}&id={id_phone}"
            response = requests.request("GET", url)
            result = json.loads(response.text)
            print(result)
            if result:
                if result["ResponseCode"] == 0:
                    data = Chaycodeso3(result["Result"])
        return data
    except:
        return None
