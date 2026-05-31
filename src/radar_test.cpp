#include <Arduino.h>
#include <ld2410.h>

ld2410 radar;
HardwareSerial radarSerial(2);

void setup() {
  Serial.begin(115200);
  Serial.println("Radar test starting...");

  radarSerial.begin(256000, SERIAL_8N1, 16, 17);

  if (radar.begin(radarSerial)) {
    Serial.println("LD2410 connected OK");
  } else {
    Serial.println("LD2410 FAILED - check wiring");
  }
}

void loop() {
  radar.read();

  const bool connected = radar.isConnected();
  const bool presence = connected && radar.presenceDetected();
  const int movCm =
      (presence && radar.movingTargetDetected()) ? (int)radar.movingTargetDistance() : -1;
  const int staCm =
      (presence && radar.stationaryTargetDetected()) ? (int)radar.stationaryTargetDistance()
                                                    : -1;

  // Uma linha por ciclo: fácil de ler no Python/plot (prefixo PLOT)
  Serial.print(F("PLOT,"));
  Serial.print(movCm);
  Serial.print(F(","));
  Serial.print(staCm);
  Serial.print(F(","));
  Serial.print(presence ? 1 : 0);
  Serial.print(F(","));
  Serial.println(connected ? 1 : 0);

  delay(200);
}