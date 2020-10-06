#include <Ethernet.h>
#include <EthernetUdp.h>
#include <SPI.h>

//sensor of thermistor
int ThermistorPin = 0;
int Vo;
float R1 = 10000;
float logR2, R2, T;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

//assign mac address ip in network or arduino

byte mac[] = { 0x98, 0x4F, 0xEE, 0x02, 0x06, 0xC3 };
IPAddress ip(103, 142,5,12); //assign any ip that arduino mapped
unsigned int localPort = 5000; //listen port can assign any
char packetBuffer[UDP_TX_PACKET_MAX_SIZE];
String Request; //string to read
EthernetUDP Udp;
int packetSize;
IPAddress server(103,142,5,14); //ip server to send back

void setup(){
    Serial.begin(9600);//Turn on Serial Port for programming and config only
    Ethernet.begin(mac,ip);
    
    system("chmod 666 /dev/ttyAM0");
    system("ifconfig eth0 > /dev/ttyAM0");
    system("chmod +x /sketch/sketch.elf");
    Udp.begin(localPort); //Start listen to port
}

void loop(){
    packetSize = Udp.parsePacket();

    //check if there anyone send
    if(packetSize>0){
        Udp.read(packetBuffer,UDP_TX_PACKET_MAX_SIZE);
        String Request(packetBuffer);
        //check request if get temperature string so send temperature back
        //do that is less error
        if (Request == "temperature"){
            Vo = analogRead(ThermistorPin);
            R2 = R1 * (1023.0 / (float)Vo - 1.0);
            logR2 = log(R2);
            T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
            T = T - 273.15;
            Udp.beginPacket(server,localPort); //initialize server and port to send
            Udp.print(T); //send temp to that port
            Udp.endPacket();
        }
        memset(packetBuffer, 0, UDP_TX_PACKET_MAX_SIZE); //reset
    }
}
