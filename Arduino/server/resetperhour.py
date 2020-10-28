import time
import requests
while(True):
    time.sleep(3600)
    r =requests.get("https://192.168.51.212/resetperhour/",verify=False)
    
