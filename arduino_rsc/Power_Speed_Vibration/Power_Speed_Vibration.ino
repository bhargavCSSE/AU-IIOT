#include <ADXL345.h>

#include <Adafruit_ADS1015.h>

#include <Wire.h>

Adafruit_ADS1115 ads1115;
ADXL345 adxl;

float inst_current, duration;
int pin = 5;
int x,y,z;
double xyz[3];
  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ads1115.begin();
  adxl.powerOn();
  ads1115.setGain(GAIN_TWO);
  pinMode(pin, INPUT);
}

void loop() {
  inst_current = (ads1115.readADC_Differential_0_1() * 0.12500381)*30/1000;
  duration = pulseIn(pin, HIGH, 1000000); 
  adxl.readXYZ(&x,&y,&z);
  adxl.getAcceleration(xyz);
  Serial.print("Current,");
  Serial.print(inst_current);
  Serial.print(",RPM,");
  Serial.print(1/(duration/100000/60));
  Serial.print(",X,"); Serial.print(x);
  Serial.print(",Y,"); Serial.print(y);
  Serial.print(",Z,"); Serial.print(z);
  Serial.print(",aX,"); Serial.print(xyz[0]);
  Serial.print(",aY,"); Serial.print(xyz[1]);
  Serial.print(",aZ,"); Serial.println(xyz[2]);
}
