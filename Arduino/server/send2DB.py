from socket import * 
import time
import datetime
from pymongo import MongoClient
import pymongo

address = ('103.142.5.12',5000)   #address to send
client_socket = socket(AF_INET,SOCK_DGRAM) #using user diagram protocol to send
client_socket.settimeout(1) # wait only 1 second
client_socket.bind(('103.142.5.14',5000)) #bind the ip to listen from arduino

#db
myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["TempDBS"]
mycol= mydb["adminpage_temperatureroom"]


while True:
    data = "temperature"
    client_socket.sendto(str.encode(data),address) #send to recieve data
    try:
        rec_data ,addr =client_socket.recvfrom(2048)
        decode_data = rec_data.decode()
        count = 1
        print(decode_data)
        datetime_object = datetime.datetime.now()
        for i in mycol.find():
            count+=1
        mytemperature = [{
			"id":count,
			"room_id":7,
			"Temperature":float(decode_data),
			"date_and_time":datetime_object,
		}
	    ]
        databasemany = mycol.insert_many(mytemperature)
        
    except:
        pass
    time.sleep(1)

