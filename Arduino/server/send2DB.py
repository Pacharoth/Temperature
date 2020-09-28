from socket import * 
import time
from pymongo import MongoClient
import pymongo

address = ('192.168.100.35',5000)   #address to send
client_socket = socket(AF_INET,SOCK_DGRAM) #using user diagram protocol to send
client_socket.settimeout(1) # wait only 1 second
client_socket.bind(('192.168.100.35',5000)) #bind the ip to listen from arduino

#db
myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["tempDBS"]
mycol= mydb["homegraph_temperature"]


while True:
    data = "temperature"
    client_socket.sendto(str.encode(data),address) #send to recieve data
    try:
        rec_data ,addr =client_socket.recvfrom(2048)
        decode_data = rec_data.decode()
        count = 1
        datetime_object = datetime.datetime.now()
        for i in mycol.find():
            count+=1
        mytemperature = [{
			"id":count,
			"room_id_id":1,
			"temperature_data":float(decode_data),
			"date_temperature":datetime_object,
		}
	    ]
        databasemany = mycol.insert_many(mytemperature)
    except:
        pass
    time.sleep(1)

