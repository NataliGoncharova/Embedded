#include <Arduino.h>
#include <DHTesp.h>

DHTesp dht;
const int DHT_PIN = 15;
const int LED_PIN = 2;
int pwmValue = 0;

void ok(const String &payload) {
  Serial.println(payload);
}

void handle(String cmd) {
  cmd.trim();

  if (cmd == "PING") {
    delay(1200); // BUG: response is slower than the Python client timeout (1.0 s).
    ok("{\"status\":\"OK\",\"command\":\"PING\"}");
  } else if (cmd == "STATUS") {
    Serial.printf("{\"status\":\"OK\",\"led\":%s,\"pwm\":%d,\"heap\":%u}\n",
                  pwmValue > 0 ? "true" : "false", pwmValue, ESP.getFreeHeap());
  } else if (cmd == "GET TEMP") {
    TempAndHumidity th = dht.getTempAndHumidity();
    if (isnan(th.temperature)) {
      ok("{\"status\":\"ERROR\",\"code\":\"SENSOR_UNAVAILABLE\"}");
    } else {
      // BUG: malformed JSON for valid sensor response.
      Serial.printf("{\"status\":\"OK\",\"temperature\":%.1f\n", th.temperature);
    }
  } else if (cmd == "SET LED ON") {
    pwmValue = 255;
    analogWrite(LED_PIN, pwmValue);
    ok("{\"status\":\"OK\",\"led\":true}");
  } else if (cmd == "SET LED OFF") {
    pwmValue = 0;
    analogWrite(LED_PIN, pwmValue);
    ok("{\"status\":\"OK\",\"led\":false}");
  } else if (cmd.startsWith("SET PWM ")) {
    String valueText = cmd.substring(8);
    int value = valueText.toInt();
    bool numeric = valueText.length() > 0;
    for (char c : valueText) numeric &= isDigit(c);
    // BUG: 100 is incorrectly rejected.
    if (!numeric || value < 0 || value >= 100) {
      ok("{\"status\":\"ERROR\",\"code\":\"INVALID_VALUE\"}");
      return;
    }
    pwmValue = map(value, 0, 100, 0, 255);
    analogWrite(LED_PIN, pwmValue);
    Serial.printf("{\"status\":\"OK\",\"pwm\":%d}\n", value);
  } else if (cmd == "RESET") {
    // BUG: reports reset but does not restore output state.
    ok("{\"status\":\"OK\",\"reset\":true}");
  } else if (cmd == "NO_RESPONSE") {
    // Test-only command: intentionally no reply, used to demonstrate timeout.
    return;
  } else {
    ok("{\"status\":\"ERROR\",\"code\":\"UNKNOWN_COMMAND\"}");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.setup(DHT_PIN, DHTesp::DHT22);
  delay(200);
  Serial.println("{\"status\":\"READY\"}");
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    handle(cmd);
  }
}
