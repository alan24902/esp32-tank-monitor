# V6 Watct Dog Timer added

import network
import espnow
from machine import Pin, I2C, WDT
import ssd1306
import time

wdt = WDT(timeout=10000)


# ===== OLED Setup =====
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)


# ===== BUZZER Setup =====
buzzer = Pin(18, Pin.OUT)
buzzer.value(0)

# ===== ESP-NOW Setup =====
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

e = espnow.ESPNow()
e.active(True)

# ===== Center text helper =====
def center_x(text):
    return int((128 - len(text) * 8) / 2)

print("Receiver ready")

oled.fill(0)
waiting_screen = center_x("Esperando Datos")    
oled.text("Esperando Datos",waiting_screen,30)
oled.show() 


last_packet_time = time.time()

# ===== Main Loop =====
while True:
    
    wdt.feed()
    
    host, msg = e.recv(timeout_ms=1000)
    
    if msg:
        last_packet_time = time.time()  # Reset the heartbeat countdown timer
    
        try:
            data = msg.decode().split(",")

            percent = int(float(data[1]))
            percent_str = "{}%".format(percent)
            
            # Getting liters
            liters = int(float(data[2]))
            liters_str = "{}L".format(liters)
            
            # Time
            time_str = data[3]

            print(percent_str, liters_str)

            # ===== OLED Display =====
            oled.fill(0)
            oled.text(time_str, 0, 0)

            x = center_x(percent_str)
            oled.text(percent_str, x, 30)
            
            l = center_x(liters_str)
            oled.text(liters_str, l, 50)
            
            oled.show()

            # ===== 🔔 Buzzer Logic =====
            if percent <= 50:
                # Beep pattern (clean, not annoying)
                buzzer.value(1)
                time.sleep(0.2)
                buzzer.value(0)
                time.sleep(0.8)
            else:
                buzzer.value(0)

        except Exception as err:
            print("Error decoding", err)
            
    # Local Signal Link Fail-Safe Protocol
    # If more than 30 seconds pass without a packet, flag it as a connection drop
    if time.time() - last_packet_time > 30:
        oled.fill(0)
        oled.text("!ERROR!", 10, 15)
        oled.text("Transmisor", 0, 35)
        oled.text("offline", 24, 48)
        oled.show()
        
    

