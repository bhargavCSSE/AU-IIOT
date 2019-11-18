#include "EmonLib.h"
// Include Emon Library
EnergyMonitor emon1;
// Create an instance
void setup()
{
  Serial.begin(9600);

  emon1.current(6, 30);             // Current: input pin, calibration.
}

void loop()
{
double Irms = emon1.calcIrms(1200);  // Calculate Irms only
Serial.print(Irms*120.0);           // Apparent power
  Serial.print(" ");
  Serial.println(Irms);             // Irms
}
