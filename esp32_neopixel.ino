/*
  Rui Santos
  Complete project details at Complete project details at https://RandomNerdTutorials.com/esp32-http-get-open-weather-map-thingspeak-arduino/

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include "Adafruit_NeoPixel.h"
#define LED_COUNT 5
#define LED_PIN 16
Adafruit_NeoPixel strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

const char* ssid = "Your SSID";
const char* password = "YOUR WIFIF password";
char myData[20];

// Your Domain name with URL path or IP address with path
String openWeatherMapApiKey = "Your API key";
// Example:
//String openWeatherMapApiKey = "bd939aa3d23ff33d3c8f5dd1dd435";

// Replace with your country code and city
String lat = "16.0544";
String lon = "108.2022";

// THE DEFAULT TIMER IS SET TO 10 SECONDS FOR TESTING PURPOSES
// For a final application, check the API call limits per hour/minute to avoid getting blocked/banned
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 10 seconds (10000)
unsigned long timerDelay = 10000;

String jsonBuffer;

void setup() {
  Serial.begin(115200);
  strip.begin();
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Timer set to 10 seconds (timerDelay variable), it will take 10 seconds before publishing the first reading.");
}

void loop() {
  // Send an HTTP GET request
  if ((millis() - lastTime) > timerDelay) {
    // Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {
      String serverPath = "http://api.openweathermap.org/data/2.5/air_pollution?lat=16.0544&lon=108.2022&appid=Your API Key goes here";  //Faff because I don't understand strings

      jsonBuffer = httpGETRequest(serverPath.c_str());
      Serial.println(jsonBuffer);
      JSONVar myObject = JSON.parse(jsonBuffer);

      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }

      Serial.print("JSON object = ");
      Serial.println(myObject);
      Serial.print("Pollution: ");
      Serial.println(myObject["list"][0]["main"]["aqi"]);
      int range = myObject["list"][0]["main"]["aqi"];

      // do something different depending on the range value:
      switch (range) {
        case 1:                         //
          Serial.println("Excellent");  //LawnGreen
          strip.fill(strip.Color(124, 252, 0));
          strip.show();
          delay(1000);
          break;
        case 2:                    //
          Serial.println("Good");  //Yellow
          strip.fill(strip.Color(255, 255, 0));
          strip.show();
          delay(1000);
          break;
        case 3:                    //
          Serial.println("Poor");  //Orange
          strip.fill(strip.Color(255, 165, 0));
          strip.show();
          delay(1000);
          break;
        case 4:                   //
          Serial.println("Bad");  //Red
          strip.fill(strip.Color(255, 0, 0));
          strip.show();
          delay(1000);
          break;
        case 5:                     //
          Serial.println("Awful");  //FireBrick
          strip.fill(strip.Color(178, 34, 34));
          strip.show();
          delay(1000);
          break;
      }

    } else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;

  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);

  // Send HTTP POST request
  int httpResponseCode = http.GET();

  String payload = "{}";

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}
