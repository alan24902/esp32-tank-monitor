# Esp32-Tank-Monitor

## Description
This project is a low-power sensor(QDY30A) liquid level sensor connected to an ESP32 sender node that runs 24/7 to takes stable tank measurements. the data is transmitted via the ESP-NOW communication protocol to an ESP32 receiver node, which displays the tank level as a percentage, the remaining volume in liters, and the real time clock synced from an NTP server. all information is displayed on an OLED screen using the I2C communication protocol.

### Key Specs
- **Power**: Both ESP32, sender and receiver are wall plugged.
- **Sensor Type**: QDY30A Hidrostatic pressure sensor(analog output) that sits before the botton of the tank.
- **Tank Height**: The calibrated full height of `1.02m` is according of the physical placement of the sensor before the bottom of the tank floor
- **Tank Capacity**:
    * **Total Capacity**: 1,000 liters
    * **Usable Capacity**: 688 liters
    * **Note**: The usable capacity is capped at 688 liters because the water pump's pipe is positioned 21 cm above the tank floor. any water belor this point is unreachable by the pump, leaving 688 liters of active, usable volume.






