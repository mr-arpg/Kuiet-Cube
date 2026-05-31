#include <Arduino.h>
#include <ld2410.h>
#include <FastLED.h>

// --- FastLED Config ---
#define LED_PIN        5
#define NUM_LEDS       13
#define LED_TYPE       WS2811
#define COLOR_ORDER    GRB

// NOTE: Due to your strip's color order, CRGB::Red displays as Blue
#define COLOR_ON       CRGB::Green
#define COLOR_OFF      CRGB::Black

CRGB leds[NUM_LEDS];

ld2410 radar;
HardwareSerial radarSerial(2);

void setAllLEDs(CRGB color) {
  fill_solid(leds, NUM_LEDS, color);
  FastLED.show();
}

void setup() {
  Serial.begin(115200);
  Serial.println("Booting...");

  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  setAllLEDs(COLOR_OFF);
  Serial.println("FastLED initialized.");

  radarSerial.begin(256000, SERIAL_8N1, 16, 17);
  if (radar.begin(radarSerial)) {
    Serial.println("LD2410 initialized successfully.");
  } else {
    Serial.println("LD2410 FAILED - check wiring.");
  }
}

void loop() {
  radar.read();

  if (!radar.isConnected()) {
    Serial.println("Radar not connected!");
    delay(100);
    return;
  }

  if (radar.presenceDetected()) {
    setAllLEDs(COLOR_ON);
    Serial.println("Presence → Light ON");
  } else {
    setAllLEDs(COLOR_OFF);
    Serial.println("No presence → Light OFF");
  }

  delay(100);
}