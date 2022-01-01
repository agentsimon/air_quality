/**
  BasicHTTPClient.ino

  Created on: 24.05.2015

*/
#include <Adafruit_NeoPixel.h>
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#define USE_SERIAL Serial
#include <WiFiClient.h>

WiFiClient WiFiClient;

#define PIN      2
#define N_LEDS 2
// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);
uint32_t red = strip.Color(255, 0, 0);
uint32_t orange = strip.Color(255, 145, 0);
uint32_t yellow = strip.Color(255, 255, 0);
uint32_t green = strip.Color(0, 255, 0);
uint32_t blue = strip.Color(0, 0, 255);
uint32_t white = strip.Color(255, 255, 255);
uint32_t black = strip.Color(0, 0, 0);
ESP8266WiFiMulti WiFiMulti;
int number_airindex ;
const int sleepSeconds = 1000 * 60 * 60 * 3; //Sleep for 180 minutes
const int sleepSeconds_show = 1000 * 6; // 6 seconds
void setup() {
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  USE_SERIAL.begin(115200);
  // USE_SERIAL.setDebugOutput(true);

  USE_SERIAL.println();
  USE_SERIAL.println();
  USE_SERIAL.println();

  for (uint8_t t = 4; t > 0; t--) {
    USE_SERIAL.printf("[SETUP] WAIT %d...", t);
    strip.fill(blue, 0, 2); strip.show();
    USE_SERIAL.flush();
    delay(1000);
  }

  WiFiMulti.addAP("SSID", "WiFiPassword");
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    HTTPClient http;

    USE_SERIAL.println("[HTTP] begin...");
    // configure traged server and url
    // get the entry_id from airvisual
    http.begin(WiFiClient, "http://api.airvisual.com/v2/nearest_city?key=Your_Key"); //HTTP

    USE_SERIAL.println("[HTTP] GET...");
    // start connection and send HTTP header
    int httpCode = http.GET();

    // httpCode will be negative on error
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      USE_SERIAL.printf("[HTTP] GET... code: %d", httpCode);

      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        String payload = http.getString();
        // Print the string value from Thingspeak
        USE_SERIAL.println(payload);
        strip.fill(white, 0, 2); strip.show();
        delay(1000);
        //USE_SERIAL.println(number_airindex);
        if (number_airindex >= 150) {
          // do Thing A
          strip.fill(red, 0, 2); strip.show();
        }
        else if (number_airindex >= 100) {
          // do Thing B
          strip.fill(orange, 0, 2); strip.show();
        }
        else if (number_airindex >= 50) {
          // do Thing B
          strip.fill(yellow, 0, 2); strip.show();
        }
        else {
          // do Thing C
          strip.fill(green, 0, 2); strip.show();
        }
      }

    } else {
      USE_SERIAL.printf("[HTTP] GET... failed, error: %s", http.errorToString(httpCode).c_str());
    }

    http.end();


  }


  delay(sleepSeconds_show);
  //Turn the LEDs to black
  strip.fill(black ); strip.show();
  Serial.println("I'm awake, but I'm going into deep sleep mode until RESET pin is connected to a LOW signal");
  ESP.deepSleep(0);

}

void loop() {

}
