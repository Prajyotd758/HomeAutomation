#include <SoftwareSerial.h>
#include <NewPing.h>
#define RELAY1 3
#define RELAY2 2
#define RELAY3 4
#define RELAY4 5

NewPing sonar(11, 10 , 15);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(RELAY1 , OUTPUT);
  pinMode(RELAY2 , OUTPUT);
  pinMode(RELAY3 , OUTPUT);
  pinMode(RELAY4 , OUTPUT);
}

void loop() {
  delay(150);
  // put your main code here, to run repeatedly:
  unsigned int value = sonar.ping();
  if(sonar.ping_cm(value) > 0 && sonar.ping_cm(value) < 5){
    digitalWrite(RELAY1 , HIGH);
    Serial.println("turnedon");
    Serial.print(sonar.ping_cm(value));
    delay(1000);
  }

  if(Serial.available()){
    // String data = Serial.readStringUntil('\n');
    char data = Serial.read();
    if(data == 'A'){
      digitalWrite(RELAY1 , HIGH);
      digitalWrite(RELAY2 , HIGH);
      digitalWrite(RELAY3 , HIGH);
    }else if(data == 'B'){
      digitalWrite(RELAY1 , LOW);
      digitalWrite(RELAY2 , LOW);
      digitalWrite(RELAY3 , LOW);
    }
    // handling single lights

    // handling hall light 
    else if(data == 'C'){
      digitalWrite(RELAY1 , HIGH);
    }else if(data == 'D'){
      digitalWrite(RELAY1 , LOW);
    }
    
    // handling bedroom light
    else if(data == 'E'){
      digitalWrite(RELAY2 , HIGH);
    }else if(data == 'F'){
      digitalWrite(RELAY2 , LOW);
    }

    //handling kitchen light
    else if(data == 'G'){
      digitalWrite(RELAY3 , HIGH);
    }else if(data == 'H'){
      digitalWrite(RELAY3 , LOW);
    }

    //handling hall fan
    else if(data == 'I'){
      digitalWrite(RELAY4 , HIGH);
    }else if(data == 'J'){
      digitalWrite(RELAY4 , LOW);
    }

    // turning on and off 2 lights
    else if(data == 'K'){
      digitalWrite(RELAY1 , HIGH);
      digitalWrite(RELAY2 , HIGH);
    }else if(data == 'L'){
      digitalWrite(RELAY1 , LOW);
      digitalWrite(RELAY2 , LOW);
    }


    else if(data == 'M'){
      digitalWrite(RELAY2 , HIGH);
      digitalWrite(RELAY3 , HIGH);
    }else if(data == 'N'){
      digitalWrite(RELAY2 , LOW);
      digitalWrite(RELAY3 , LOW);
    }


    else if(data == 'O'){
      digitalWrite(RELAY1 , HIGH);
      digitalWrite(RELAY3 , HIGH);
    }else if(data == 'P'){
      digitalWrite(RELAY1 , LOW);
      digitalWrite(RELAY3 , LOW);
    }
    else{
      Serial.print("INVALID INPUT");
    }
      // Serial.print(data);
  }
}