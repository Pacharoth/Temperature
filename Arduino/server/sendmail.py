import time
import requests
while(True):
    time.sleep(2)
    r =requests.get("http://127.0.0.1:8000/sendmail/")
    p=r.json()['data']
    for i in p:
        if i>25:
            time.sleep(3600)