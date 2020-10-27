from socket import * 
import time
import datetime
from pymongo import MongoClient
import pymongo

#address = ('192.168.1.112',5000)   #address to send
client_socket = socket(AF_INET,SOCK_DGRAM) #using user diagram protocol to send
client_socket.settimeout(1) # wait only 1 second
client_socket.bind(('192.168.51.212',5000)) #bind the ip to listen from arduino
# client_socket.listen()
#db
myclient= pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["TempDBS"]
mycol= mydb["adminpage_temperatureroom"]


while True:
    # data = "temperature"
    # client_socket.sendto(str.encode(data),address) #send to recieve data
    try:
        rec_data ,addr =client_socket.recvfrom(2048)
        decode_data = rec_data.decode()
        count = 1
        print(decode_data)
        datetime_object = datetime.datetime.now()
        for i in mycol.find():
            count = i['id']+1
        mytemperature = [{
			"id":count,
			"room_id":7,
			"Temperature":float(decode_data),
			"date_and_time":datetime_object,
		}
	]
        databasemany = mycol.insert_many(mytemperature)
        print (databasemany)
    except:
        pass
    time.sleep(1)

