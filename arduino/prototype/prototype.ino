#include <Servo.h>

#define MAIN_SPEED 40
#define MAIN_NEUTRAL 94
#define BUMP_ENGAGED 120
#define BUMP_NEUTRAL 180

Servo servo1;  // Motor.
int servo1pin = 9;
int servo1value = 0;
int servo1start = 0;
int servo1dir = 0;

Servo servo2;
int servo2pin = 10;
int servo2value = 0;
int servo2start = 0;

Servo servo3;
int servo3pin = 5;
int servo3value = 0;
int servo3start = 0;

Servo servo4;
int servo4pin = 11;
int servo4value = 0;
int servo4start = 0;

Servo servo5;
int servo5pin = 12;
int servo5value = 0;
int servo5start = 0;

int ledState = LOW;

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(5);
    
    servo1.attach(servo1pin);
    servo1value = MAIN_NEUTRAL;
    servo1.write(servo1value);

    int t = millis();

    servo2.attach(servo2pin);
    servo2value = BUMP_NEUTRAL;
    servo2.write(servo2value);
    servo2start = t;

    servo3.attach(servo3pin);
    servo3value = BUMP_NEUTRAL;
    servo3.write(servo3value);
    servo3start = t;

    servo4.attach(servo4pin);
    servo4value = BUMP_NEUTRAL;
    servo4.write(servo4value);
    servo4start = t;

    servo5.attach(servo5pin);
    servo5value = BUMP_NEUTRAL;
    servo5.write(servo5value);
    servo5start = t;
    
    pinMode(13, OUTPUT);
    //digitalWrite(13, ledState);
}

void loop() {
  switch (readData()) {
    case 1:
      // Stops the main servo.
      servo1.write(MAIN_NEUTRAL);
      servo1start = millis() - servo1start;
      servo1value += servo1start * servo1dir;
      servo1dir = 0;
      break;
    case 2:
      // Moves the main servo in one direction.
      servo1.write(MAIN_NEUTRAL - MAIN_SPEED);
      servo1start = millis();
      servo1dir = -1;
      break;
    case 3:
      // Moves the main servo in the other direction.
      servo1.write(MAIN_NEUTRAL + MAIN_SPEED);
      servo1start = millis();
      servo1dir = 1;
      break;
    case 4:
      // Reads the main servo position.
      Serial.println(servo1value + (millis() - servo1start) * servo1dir);
      break;
    case 5:
      // Reads the servo positions.
      if (servo2value == BUMP_ENGAGED) {
        Serial.println(1);
      } else {
        Serial.println(0);
      }
      if (servo3value == BUMP_ENGAGED) {
        Serial.println(1);
      } else {
        Serial.println(0);
      }
      if (servo4value == BUMP_ENGAGED) {
        Serial.println(1);
      } else {
        Serial.println(0);
      }
      if (servo5value == BUMP_ENGAGED) {
        Serial.println(1);
      } else {
        Serial.println(0);
      }
      break;
    case 99:
      // Just dummy to cancel the current read, needed to prevent lock 
      // when the PC side dropped the "w" that we sent.
      break;
  }
}

char readData() {
  Serial.println("w");
  while (true) {
    if (Serial.available() > 0) {
      return Serial.parseInt();
    }
    updatePosition();
  }
}

void updatePosition() {
  int steps = (millis() - servo2start) / 1000;
  if (steps % 6 == 5) {
    if (servo2value == BUMP_NEUTRAL) {
      digitalWrite(13, HIGH);
      servo2value = BUMP_ENGAGED;
      servo2.write(servo2value);
    }
  } else {
    if (servo2value == BUMP_ENGAGED) {
      digitalWrite(13, LOW);
      servo2value = BUMP_NEUTRAL;
      servo2.write(servo2value);
    }
  }

  if (steps % 8 < 3) {
    if (servo3value == BUMP_NEUTRAL) {
      servo3value = BUMP_ENGAGED;
      servo3.write(servo3value);
    }
  } else {
    if (servo3value == BUMP_ENGAGED) {
      servo3value = BUMP_NEUTRAL;
      servo3.write(servo3value);
    }
  }

  if (steps % 5 < 2) {
    if (servo4value == BUMP_NEUTRAL) {
      servo4value = BUMP_ENGAGED;
      servo4.write(servo4value);
    }
  } else {
    if (servo4value == BUMP_ENGAGED) {
      servo4value = BUMP_NEUTRAL;
      servo4.write(servo4value);
    }
  }

  if (steps % 7 > 4) {
    if (servo5value == BUMP_NEUTRAL) {
      servo5value = BUMP_ENGAGED;
      servo5.write(servo5value);
    }
  } else {
    if (servo5value == BUMP_ENGAGED) {
      servo5value = BUMP_NEUTRAL;
      servo5.write(servo5value);
    }
  }
}

