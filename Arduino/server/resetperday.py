import time
import requests
while(True):
    time.sleep(24*3600)
    r =requests.get("https://192.168.51.212/resetperday/",verify=False)
    
