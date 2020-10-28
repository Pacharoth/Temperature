import time
import requests
while(True):
    time.sleep(2)
<<<<<<< HEAD
    r=requests.get("https://192.168.51.212/sendmail",verify=False)
    print(r)
=======
    r =requests.get("http://127.0.0.1:8000/sendmail/")
>>>>>>> 0cdb3dfeb662914fc994753152faa4895c97e6a0
    p=r.json()['data']
    for i in p:
        if i>25:
            time.sleep(3600)