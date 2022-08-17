byte PWM_PIN = 2;
byte logic_out_pin = 3;
 
int pwm_value;
 
void setup() {
  pinMode(PWM_PIN, INPUT);
  pinMode(logic_out_pin, OUTPUT);
  digitalWrite(logic_out_pin, HIGH);
  Serial.begin(115200);
}
 
void loop() {
  pwm_value = pulseIn(PWM_PIN, HIGH);

  if(pwm_value > 1200) {
    digitalWrite(logic_out_pin, LOW);
    delay(10);
  }
  else {
    digitalWrite(logic_out_pin, HIGH);
    delay(10);
  }
  Serial.println(pwm_value);
}
