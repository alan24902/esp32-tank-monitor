# Esp32-Tank-Monitor

## Description
This project is a low-power QDY30A hydrostatic liquid level sensor connected to an ESP32 sender node that runs 24/7 to take stable tank measurements. The data is transmitted via the ESP-NOW communication protocol to an ESP32 receiver node, which displays the tank level as a percentage, the remaining volume in liters, and the real time clock synced from an NTP server. All information is displayed on an OLED screen using the I2C communication protocol. Additionally, an active buzzer is activated when the water level is drops below50%, triggerring an audible alarm to alert users of a low water state. In addition to the main nodes, the system includes a diagnostic tool build on a Heltec v3 to run a quick diagnostic report readings. This diagnostic interface supports two communications methods: ESP-NOW and UART. Lastly, an external Heltec v3 is used to calibrate the hydrostatic sensor. 

### Key Specs
- **Power**: 
    * **ESP32**: Both ESP32, sender and receiver are wall plugged with operating voltage 5V DV via USB-C wall adapters.
    * **QDY30A**: The hydrostatic sensor powered by the 5V output that the ESP32 provides.
- **Sensor Type**: QDY30A Hidrostatic pressure sensor(analog output, 0-3.3V 5DC) that sits before the botton of the tank.
- **Tank Height**: The calibrated full height of `1.02m` is according of the physical placement of the sensor before the bottom of the tank floor
- **Tank Capacity**:
    * **Total Capacity**: 1,000 liters
    * **Usable Capacity**: 688 liters
    * **Note**: The usable capacity is capped at 688 liters because the water pump's pipe is positioned 21 cm above the tank floor. any water belor this point is unreachable by the pump, leaving 688 liters of active, usable volume.
- **Connectivity**: 
    * **ESP-NOW**: Establish a wireless communication between the ESP32 transmmiter and the ESP32 receiver for a real-time data sharing, also connects the wireless diagnostic tool device. 
    * **Wi-Fi (NTP)**: The ESP32 sender node uses Wi-Fi to syncronize the local internal RTC with the NTP server and fetches the time.
    * **UART**: A hardwired interface connecting the ESP32 sender node to the Heltec diagnostic deveice to read the data and display it in the Heltec built-in oled screen. 

### Hardware
## Core electronics
- **ESP32**:
    * **ESP32 Wroom 32U**:
    * **ESP32 Wroom 32D**:




\


