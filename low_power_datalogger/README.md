# Low Power Dtatlogger
Using a Arduino MCU to log data into SD card by a csv file. the MCU will weakup 10 minutes and write 5 rows data into the file.

### Basic Design
* SD card is reading through SPI lines. it will need some of the buffer to protect the circuits. also EMI/ESD protected is needed to the circuits too. SN74HCS125 can be used for the buffer, and the TPD6F003 can be used for ESD and EMI protection.
* There will be two control signal lines for the SD card. one is the switch on the socket, the MCU can use that to detected if the SD card has inserted. another one is the GPIO from MCU to turn on/off the power line for the SD card by using a P-MOSFET. Adding feature to turn on/off the SD card power will help to reduce teh power cost.
* for MCU, I will pick nordic nRF52 MCU, which has super low standby current and can be programmed by arduino. but it will cost a little bit more.
* 


### tools
* VS Code: text editor
* Arduino IDE: coding
* google and chatgpt: searching and coding help