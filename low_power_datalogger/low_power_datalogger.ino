#include <SPI.h>
#include <SD.h>

#define SD_CS   4 // for SD library, only CS pin need to be selected, all other spi pins are using default.
#define SD_PWR  5

int fileIndex = 0;

void setup() {
  pinMode(SD_PWR, OUTPUT);
  digitalWrite(SD_PWR, HIGH); // default power off
}

void loop() {
  // Wake every 10mins
  delay(600000);  // 10min = 600000 ms

  // turn on sd card power
  digitalWrite(SD_PWR, LOW);
  delay(100);

  if (SD.begin(SD_CS)) {
    String filename = "LOG" + String(fileIndex++) + ".CSV"; // the file name can changed maybe using random or time
    File file = SD.open(filename, FILE_WRITE);
    if (file) {
      for (int i = 0; i < 5; i++) {
        file.println("Row " + String(i) + ",123,456");
      }
      file.close();
    }
    SD.end();
  }

  // turn off sd card power
  digitalWrite(SD_PWR, HIGH);
}