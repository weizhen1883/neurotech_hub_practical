# Low Power Dtatlogger
Using a Arduino MCU to log data into SD card by a csv file. the MCU will weakup 10 minutes and write 5 rows data into the file.

### Basic Design
* SD card is reading through SPI lines. it will need some of the buffer to protect the circuits. also EMI/ESD protected is needed to the circuits too. SN74HCS125 can be used for the buffer, and the TPD6F003 can be used for ESD and EMI protection.
* There will be two control signal lines for the SD card. one is the switch on the socket, the MCU can use that to detected if the SD card has inserted. another one is the GPIO from MCU to turn on/off the power line for the SD card by using a P-MOSFET. Adding feature to turn on/off the SD card power will help to reduce teh power cost.
* for MCU, I will pick nordic nRF52 MCU, which has super low standby current and can be programmed by arduino. but it will cost a little bit more.

### Notes
the code [low_power_datalogger.ino](low_power_datalogger.ino) is a very sample code to do the basic feature. it compiled, but not test run on the real hardware. I do not have this hardware on hands.

the power cost for this program will be high, since delay only put the mcu into idle mode, which is in 1 to 2mA range, but it will have the feature to using its own sdk or zephyr rtos to get the access to deeper low power mode, which will reduce the sleep power to 1.5uA with a clock to weak up.

on the data logging time, MCU + SD card read/write, the system will take around 30 to 50mA.


### tools
* VS Code: text editor
* Arduino IDE: coding
* google and chatgpt: searching and coding help