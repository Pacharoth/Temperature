from socket import * 
import time
import datetime
from pymongo import MongoClient
import pymongo
from pytz import timezone
from django.utils.timezone import now,activate,localtime 
# client_socket.listen()
#db
myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["TempDBS"]
mycol= mydb["adminpage_temperatureroom"]


while True:
    # data = "temperature"
    # client_socket.sendto(str.encode(data),address) #send to recieve data
    count=1
    datetime_object = datetime.datetime.now(timezone('Asia/Phnom_Penh')).strftime("%Y-%m-%dT%H:%M:%S%z")
    convertTodateTime =datetime.datetime.strptime(datetime_object,"%Y-%m-%dT%H:%M:%S%z")
    
    # print(convertTodateTime)
    for i in mycol.find():
        count = i['id']+1
    mytemperature = [{
        "id":count,
        "room_id":1,
        "Temperature":26,
        "date_and_time":convertTodateTime,
    }
	]
    print(datetime_object)
    databasemany = mycol.insert_many(mytemperature)
    time.sleep(1)

# import time
# import requests
# while(True):
#     time.sleep(2)
#     r=requests.get("http://127.0.0.1:8000/sendmail",verify=False)
#     print(r)
#     p=r.json()['data']
#     for i in p:
#         if i>25:
#             time.sleep(60)
#             break