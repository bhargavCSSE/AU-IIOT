#define sensorPin  5

void setup() {
  pinMode(sensorPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int sensed = digitalRead(sensorPin);
  if(sensed == HIGH){
    Serial.println(sensed*5);
  }else{
    Serial.println(sensed);
  }
}
 
