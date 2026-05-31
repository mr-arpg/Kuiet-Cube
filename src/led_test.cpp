#include <Arduino.h>
#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    13
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  fill_solid(leds, NUM_LEDS, CRGB::Red);
  FastLED.show();
}

void loop() {}