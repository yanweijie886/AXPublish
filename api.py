import requests


def addlog(data):
    url = "http://192.168.30.55:5000/add/updataLog"
    res = requests.post(url, data=data.encode())
    print(res.text)
