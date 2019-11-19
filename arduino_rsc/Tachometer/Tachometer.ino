#define sensorPin  5
double last = 0;
double time_between_pulses = 0;

void setup() {
  pinMode(sensorPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int sensed = digitalRead(sensorPin);
  if(sensed == HIGH){
    //Serial.println(sensed*5);
    time_between_pulses = millis()-last;
    last = millis();
    
    Serial.println(time_between_pulses);
  }
  
  else{
    //Serial.println(sensed);
  }
}
 
