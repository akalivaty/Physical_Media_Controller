#include <Arduino.h>
#include <SoftwareSerial.h>

#define PHOTOR_THRESHOLE 400 // depends on the photoresistor
#define VOLUME_THRESHOLE 20

SoftwareSerial BTserial(2, 3); // SoftwareSerial(RX, TX) on arduino board

const uint8_t button1 = 6;
const uint8_t button2 = 7;
const uint8_t photoR = A0;
const uint8_t potentiometer = A1;

uint8_t c = ' ';
bool NL = true;
uint16_t photoR_avg = 0;
int16_t volume = 0; // 0 - 1023
int16_t volume_prev = 0;
int8_t filterVolume = 0;
int8_t conversionVolume = 0;
int8_t conversionVolume_prev = 0;

void MainProcess();
void BTProcess();
int16_t VolumeFilter_1(int16_t);
int8_t VolumeFilter_2(int8_t);

void setup()
{
  Serial.begin(115200);
  BTserial.begin(38400);

  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(photoR, INPUT);
  pinMode(potentiometer, INPUT);

  Serial.print("Sketch:   ");
  Serial.println(__FILE__);
  Serial.print("Uploaded: ");
  Serial.println(__DATE__);
  Serial.println("");
}

void loop()
{
  MainProcess();
  BTProcess();
}

void MainProcess()
{
  volume = (analogRead(potentiometer));
  filterVolume = VolumeFilter_2(VolumeFilter_1(volume));
  if (filterVolume != -1)
  {
    BTserial.write("volume:");
    BTserial.write(filterVolume);
    BTserial.write("\n");

    // Serial.write("write_volume:");
    // Serial.write(volume);
    // Serial.write('\n');
    Serial.print("print_volume:");
    Serial.println(filterVolume);
  }
  if (digitalRead(button1) == LOW)
  {
    BTserial.write("btn1\n");
    Serial.write("btn1\n");
    delay(50);
  }
  if (digitalRead(button2) == LOW)
  {
    BTserial.write("btn2\n");
    Serial.write("btn2\n");
    delay(50);
  }
  if (analogRead(photoR) < PHOTOR_THRESHOLE)
  {
    BTserial.write("photoR\n");
    Serial.write("photoR\n");
    delay(300);
  }
  delay(100);
}

void BTProcess()
{
  if (BTserial.available())
  {
    c = BTserial.read();
    Serial.write(c);
  }

  if (Serial.available())
  {
    // for example, "at" will be read 4 times:
    // 97 -> 116 -> 13 -> 10, a -> t -> CR -> NL in ASCII
    c = Serial.read();
    BTserial.write(c);

    // to hold up the first character in an inputted message
    if (NL)
    {
      Serial.print(">>> ");
      NL = false;
    }

    Serial.write(c);

    // if meeting the end of the inputted message, print >>> next time
    if (c == 10)
    {
      NL = true;
    }
  }
}

int16_t VolumeFilter_1(int16_t volume)
{
  // Serial.print("VolumeFilter_1: ");
  // Serial.print(volume);
  // Serial.print(" volume_prev: ");
  // Serial.println(volume_prev);

  if (!(volume_prev - VOLUME_THRESHOLE < volume && volume < volume_prev + VOLUME_THRESHOLE))
  {
    volume_prev = volume;
    conversionVolume = map(volume, 0, 1023, -5, 105); // the value depends on the potentiometer precision
    if (conversionVolume < 0)
    {
      return 0;
    }
    if (conversionVolume > 100)
    {
      return 100;
    }
    return conversionVolume;
  }
  return -1;
}

int8_t VolumeFilter_2(int8_t volume)
{
  if (volume != -1 && conversionVolume_prev != volume)
  {
    conversionVolume_prev = volume;
    return volume;
  }
  return -1;
}