
int power = 1;

void setup()
{
   Serial.begin(9600);
   while(!Serial) {
    //wait for serial connection
   } 
   
    pinMode(4,OUTPUT); //The pin connected to the ATX Controller
 }
 
 void loop()
 {
   
   if(power==48)
   {
     Serial.println("Turning On the SoCDrawer.");
     digitalWrite(4,LOW);
   }
   
   if(power==49)
   {
      Serial.println("Turning OFF the SoCDrawer.");
      digitalWrite(4,HIGH); 
   }
     
   if (Serial.available() > 0) {
     //Data exists at the Serial channel
     power = Serial.read();
     Serial.println(power);
   }
   
 }
