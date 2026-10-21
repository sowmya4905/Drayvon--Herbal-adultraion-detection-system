#include <WiFi.h> // Provides Wi-Fi connectivity for ESP32
#include <HTTPClient.h> // Sends HTTP requests to ThingSpeak
#include <Wire.h> // Enables I2C communication for TCS34725
#include <Adafruit_TCS34725.h> // Driver library for TCS34725 RGB sensor
// ===================== Wi-Fi MODULE =====================
const char* WIFI_SSID = "YOUR_WIFI_NAME"; // Wi-Fi network name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"; // Wi-Fi password
// ===================== THINGSPEAK CLOUD MODULE =====================
const char* API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"; // ThingSpeak write API key
const char* SERVER = "http://api.thingspeak.com/update"; // ThingSpeak data upload URL
// ===================== ANALOG SENSOR MODULE =====================
#define PH_PIN 34 // ESP32 ADC pin connected to pH sensor
#define TDS_PIN 35 // ESP32 ADC pin connected to TDS sensor
// ===================== RGB SENSOR MODULE =====================
// TCS34725 measures Red, Green, Blue and Clear light intensity through I2C
Adafruit_TCS34725 tcs(
 TCS34725_INTEGRATIONTIME_50MS,
 TCS34725_GAIN_4X
);
// ===================== ADC CONFIGURATION =====================
const float VREF = 3.3; // ESP32 ADC reference voltage
const int ADC_MAX = 4095; // 12-bit ADC maximum value
// ===================== DATA UPLOAD TIMING =====================
unsigned long lastUpload = 0; // Stores previous upload time
const unsigned long uploadInterval = 20000; // ThingSpeak upload interval = 20 seconds
// =========================================================
// SETUP MODULE
// Initializes sensors, ADC, I2C and Wi-Fi
// =========================================================
void setup()
{
 Serial.begin(115200); // Starts serial communication for monitoring
 analogReadResolution(12); // Configures ESP32 ADC with 12-bit resolution
 Wire.begin(); // Starts I2C communication for RGB sensor
 // ---------- Initialize TCS34725 RGB Sensor ----------
 if (!tcs.begin())
 {
 Serial.println("TCS34725 not detected!");
 while (1); // Stop execution if RGB sensor is unavailable
 }
 Serial.println("TCS34725 detected.");
 // ---------- Connect ESP32 to Wi-Fi ----------
 WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 Serial.print("Connecting to Wi-Fi");
 while (WiFi.status() != WL_CONNECTED)
 {
 delay(500);
 Serial.print(".");
 }
 Serial.println();
 Serial.println("Wi-Fi Connected!");
 Serial.print("IP Address: ");
 Serial.println(WiFi.localIP());
}
// =========================================================
// MAIN LOOP
// Continuously reads sensors and uploads data
// =========================================================
void loop()
{
 // Reconnect to Wi-Fi if connection is lost
 if (WiFi.status() != WL_CONNECTED)
 {
 WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 }
 // =======================================================
 // pH SENSOR MODULE
 // Reads analog voltage corresponding to sample acidity
 // =======================================================
 int phADC = analogRead(PH_PIN); // Read raw ADC value
 float phVoltage =
 (phADC * VREF) / ADC_MAX; // Convert ADC value to voltage
 // Calibration equation; replace with actual sensor calibration
 float pH =
 7.0 + ((2.5 - phVoltage) / 0.18);
 // =======================================================
 // TDS SENSOR MODULE
 // Measures dissolved-solid concentration using conductivity
 // =======================================================
 int tdsADC = analogRead(TDS_PIN); // Read raw TDS ADC value
 float tdsVoltage =
 (tdsADC * VREF) / ADC_MAX; // Convert ADC value to voltage
 // Calibration approximation; replace with actual calibration
 float TDS =
 tdsVoltage * 300.0;
 // =======================================================
 // RGB SENSOR MODULE
 // Measures optical/color characteristics of the sample
 // =======================================================
 uint16_t R, G, B, C;
 tcs.getRawData(&R, &G, &B, &C); // Read raw RGB and clear values
 // =======================================================
 // SERIAL MONITOR MODULE
 // Displays sensor values for testing and debugging
 // =======================================================
 Serial.println();
 Serial.println("========== DRAVYON ==========");
 Serial.print("pH : ");
 Serial.println(pH, 2);
 Serial.print("TDS : ");
 Serial.print(TDS, 2);
 Serial.println(" ppm");
 Serial.print("Red : ");
 Serial.println(R);
 Serial.print("Green : ");
 Serial.println(G);
 Serial.print("Blue : ");
 Serial.println(B);
 Serial.println("=============================");
 // =======================================================
 // CLOUD COMMUNICATION MODULE
 // Uploads sensor data to ThingSpeak using HTTP
 // =======================================================
 if (millis() - lastUpload >= uploadInterval)
 {
 if (WiFi.status() == WL_CONNECTED)
 {
 HTTPClient http;
 // Map sensor values to ThingSpeak fields
 String url =
 String(SERVER) +
 "?api_key=" + API_KEY +
 "&field1=" + String(pH, 2) +
 "&field2=" + String(TDS, 2) +
 "&field3=" + String(R) +
 "&field4=" + String(G) +
 "&field5=" + String(B);
 http.begin(url); // Initialize HTTP connection
 int responseCode = http.GET(); // Send data to ThingSpeak
 // Check whether upload was successful
 if (responseCode > 0)
 {
 Serial.print("ThingSpeak Response: ");
 Serial.println(responseCode);
 Serial.print("Entry ID: ");
 Serial.println(http.getString());
 }
 else
 {
 Serial.print("Upload Error: ");
 Serial.println(responseCode);
 }
 http.end(); // Close HTTP connection
 }
 lastUpload = millis(); // Store latest upload time
 }
 delay(1000); // Delay before next sensor reading
}void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
