NodeMcu Code

<pre>
include "Nextion.h"
include "HX711.h"
include "UbidotsMicroESP8266.h"
define TOKEN "A1E-YWTxyQZ8m6vIuPbPiKHQT5oRd3DZJI" // Put your Ubidots
TOKEN here
define WIFISSID "hotspot name" // Put here your Wi-Fi SSID
define PASSWORD "password" // Put here your Wi-Fi password
Ubidots client(TOKEN);
// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 15; //D8
const int LOADCEL_SCK_PIN = 13; //D7
HX711 scale;
//pulse
int p=4;
int c=0;
int a;
float t;
bool f=false;
//range
// defines pins numbers
const int trigPin = 2; //D4
const int echoPin = 0; //D3
// defines variables
long duration;
int distance;
int reading ;
int bindex;
// Declare your Nextion objects - Example (page id = 0, component id = 1, com-
ponent name = "b0")
//page 0
NexButton measure = NexButton(0, 1, "b0");
//page 1
NexText BMI = NexText(1, 1, "t0");20
Appendix A. System Code
NexText HR = NexText(1, 2, "t1");
NexButton h1 = NexButton(1, 3, "b0");
//page 2
NexButton h2 = NexButton(2, 1, "b0");
NexButton b1 = NexButton(2, 2, "b1");
NexNumber ht = NexNumber(2, 4, "n0");
NexNumber wt = NexNumber(2, 6, "n1");
NexNumber bmi = NexNumber(2, 8, "n2");
//page 3
NexButton h3 = NexButton(3, 1, "b0");
NexButton b2 = NexButton(3, 2, "b1");
NexNumber hr = NexNumber(3, 4, "n0");
// Register a button object to the touch event list.
NexTouch *nex_listen_list[] = {
&measure,
&BMI,
&HR,
&h1,
&h2,
&b1,
&h3,
&b2,
NULL
};
void fitcal(void *ptr) {
ht.setValue(172);//reading height
wt.setValue(reading) ; //reading weight
bmi.setValue(bindex); //reading bmi
ht.setValue(distance);//reading height
}
void hrcal(void *ptr) {
hr.setValue(88) ; //reading heart rate value
hr.setValue(c);//reading height
}
void setup() {
pinMode(p,INPUT);
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
// You might need to change NexConfig.h file in your ITEADLIB_Arduino_Nextion
folder
// Set the baudrate which is for debug and communicate with Nextion screen
Serial.begin(9600);
nexInit();
// Register the pop event callback function of the componentsAppendix A. System Code
21
BMI.attachPop(fitcal, BMI);
HR.attachPop(hrcal, HR);
scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
yield();
client.wifiConnection(WIFISSID, PASSWORD);
client.setDebug(true); // Uncomment this line to set DEBUG on
client.setDataSourceName("Fitness kiosk");
client.setDataSourceLabel("fitness-kiosk");
}
void loop() {
Serial.println("start");
/* When a pop or push event occured every time, the corresponding component
[right page id and component id] in touch event list will be asked. */
yield();
//pulse start
c=0;
yield();
t=millis();
while(millis()-t<15000)
{
yield();
a=digitalRead(p);
if(a==HIGH f==false)
{
c=c+1;
f=true;
}
if(a==LOW)
{
yield();
f=false;
}
yield();
}
Serial.print("BPM:");
yield();
c=c*4;
Serial.println(c);
// pulse stop yield();
//range start
// Clears the trigPin
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds22
Appendix A. System Code
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance= duration*0.034/2;
// Prints the distance on the Serial Monitor
Serial.print("Height: ");
distance=197-distance;
Serial.println(distance);
delay(2000);
//range stop
yield();
//weight start
if (scale.is ready()) {
reading = scale.read();
reading=(reading* -0.035274)/1580;
Serial.print("HX711 reading: ");
Serial.println(reading);
}
else { Serial.println("HX711 not found."); }
delay(1000);
yield();
//weight done
// Calculating the BMI
bindex=(reading*100*100/(distance*distance));
// Prints the distance on the Serial Monitor Serial.print("BMI: ");
Serial.print(bindex);
// BMI done
yield();
nexLoop(nex listen list);
yield();
client.add("BPM", c);
client.add("BMI", bindex);
client.add("Height", distance);
client.add("Weight", reading );
client.sendAll(true);
}

</pre>
