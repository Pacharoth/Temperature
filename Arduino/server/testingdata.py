import random
import time
from pymongo import MongoClient
import datetime
import pymongo

myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["TempDBS"]
mycol= mydb["adminpage_temperaturestore"]
while True:
    count=1
    for i in mycol.find():
        count+=1
    print(count)
    mytemperature=[{
        "id":coun,
        "room_id":109,
        "Temperature":random.randint(1,30),
        "date":datetime.datetime.now()
    }]
    time.sleep(2)
    data = mycol.insert_many(mytemperature)