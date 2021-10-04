
// digital pin 2 has a pushbutton attached to it. Give it a name:
int push_button_in = 2;

int rgb_led_out_r = 9;

int rgb_led_out_g = 10;

int rgb_led_out_b = 11;


int milliseconds_of_light = 500;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(push_button_in, INPUT);

    pinMode(rgb_led_out_r, OUTPUT);
      pinMode(rgb_led_out_g, OUTPUT);
        pinMode(rgb_led_out_b, OUTPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int button_pressed = digitalRead(push_button_in);

  if(button_pressed){
    
    digitalWrite(rgb_led_out_r, 0);
    digitalWrite(rgb_led_out_g, 0);
    digitalWrite(rgb_led_out_b, 0);
    delay(1);
    digitalWrite(rgb_led_out_r, 1);
    delay(milliseconds_of_light);
    digitalWrite(rgb_led_out_r, 0);
    digitalWrite(rgb_led_out_g, 0);
    digitalWrite(rgb_led_out_b, 0);
    delay(1);
    digitalWrite(rgb_led_out_g, 1);
    delay(milliseconds_of_light);
    digitalWrite(rgb_led_out_r, 0);
    digitalWrite(rgb_led_out_g, 0);
    digitalWrite(rgb_led_out_b, 0);
    delay(1);
    digitalWrite(rgb_led_out_b, 1);
    delay(milliseconds_of_light);
    
   }else{
    digitalWrite(rgb_led_out_r, 0);
    digitalWrite(rgb_led_out_g, 0);
    digitalWrite(rgb_led_out_b, 0);
    
   }
Serial.println(button_pressed);
  delay(1);        // delay in between reads for stability
}