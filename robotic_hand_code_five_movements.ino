//#include <NewSoftSerial.h>
#include <SoftwareSerial.h>
//#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

//NewSoftSerial mySerial(4, 2); // RX, TX

SoftwareSerial mySerial(4, 2); // RX, TX
int ledpin=13; // led on D13 will show blink on / off
int BluetoothData; // the data given from Computer

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);
// you can also call it with a different address and I2C interface
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40, &Wire);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  400 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  750 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;
// Here we store previous finger's number
uint8_t previous_finger_servo_number = 50;

void setup() {
  // put your setup code here, to run once:
  mySerial.begin(9600);
  pinMode(ledpin,OUTPUT);
  
  pwm.begin();
  
  
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  delay(10);

  // INITIALLY WE BEGIN BY CLOSING ALL FINGERS
  for (int i=0;i<5;i++)
  {
    for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) 
    {
      pwm.setPWM(i, 0, pulselen);
    }
    pwm.setPWM(0, 0, 4096);
    pwm.setPWM(1, 0, 4096);
    pwm.setPWM(2, 0, 4096);
    pwm.setPWM(3, 0, 4096);
    pwm.setPWM(4, 0, 4096);
    delay(500);
  }
}

// you can use this function if you'd like to set the pulse length in seconds
// e.g. setServoPulse(0, 0.001) is a ~1 millisecond pulse width. its not precise!
void setServoPulse(uint8_t n, double pulse) {
  double pulselength;
  
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 60;   // 60 Hz
//  Serial.print(pulselength); Serial.println(" us per period"); 
  pulselength /= 4096;  // 12 bits of resolution
//  Serial.print(pulselength); Serial.println(" us per bit"); 
  pulse *= 1000000;  // convert to us
  pulse /= pulselength;
//  Serial.println(pulse);
  pwm.setPWM(n, 0, pulse);
}

void loop() 
{
  if (mySerial.available()>0) 
  {    
    // We read the bluetooth data. In this case the finger to be moved by servo motor
    BluetoothData=mySerial.read();
    if (BluetoothData == '0')
    {
      servonum = 0;      
    }
    else if (BluetoothData == '1')
    {
      servonum = 1;
    }
    else if (BluetoothData == '2')
    {
      servonum = 2;
    }
    else if (BluetoothData == '3')
    {
      servonum = 3;
    }
    else if (BluetoothData == '4')
    {
      servonum = 4;
    }
    else
    {
      
    }
    mySerial.write(BluetoothData);
    digitalWrite(ledpin,!digitalRead(ledpin));
    // If previous finger was different than the received finger servo number then open received servo number
    if (previous_finger_servo_number != servonum)
    {
      // Open the classified finger
      for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen--) 
      {
        pwm.setPWM(servonum, 0, pulselen);
      }
      // This line stops the motor so that it doesnt keep "buzzing"
      pwm.setPWM(servonum,0,4096);      
      delay(500);
      
      // Close the previous finger
      if (previous_finger_servo_number < 5)
      {
        for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) 
        {
          pwm.setPWM(previous_finger_servo_number, 0, pulselen);
        }
      }
      // This line stops the motor so that it doesnt keep "buzzing"
      pwm.setPWM(previous_finger_servo_number,0,4096);
      
      delay(500);
      previous_finger_servo_number = servonum;
    }
    delay(100);
  }
}
