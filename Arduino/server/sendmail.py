import time
import requests
while(True):
    time.sleep(2)
    r=requests.get("https://192.168.51.212/sendmail",verify=False)
    print(r)
    p=r.json()['data']
    for i in p:
        if i>25:
            time.sleep(3600)