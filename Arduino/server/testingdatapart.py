import random
import time
from pymongo import MongoClient
import datetime
import pymongo

myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["TempDBS"]
mycol= mydb["adminpage_temperaturestore"]

count=mycol.count()+1
f=0
# for i in mycol.find():
#     count+=1
#     if count >=28:
#         p=count-1
#         p=count-p
#         f=p
        
    
# print(count)
print(count)
mytemperature=[{
    "id":count,
    "room_id":109,
    "Temperature":random.randint(1,30),
    "date":datetime.datetime(2020,10,17)
}]
# time.sleep(2)
data = mycol.insert_many(mytemperature)