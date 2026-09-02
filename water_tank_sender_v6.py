# v6 wifi reconection improved for time
# Now the esp32 sender can keep working even if there is not wifi available

import network
import espnow
from machine import ADC, Pin, WDT, UART
import time
import ntptime


# Home receiver MAC
HOME_MAC = b'\x84\x1f\xe8i l'


# Portable Receiver MAC
PORTABLE_MAC = b'\xac\xa7\x043\x13\xe0'


def init_espnow():
    global e

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    try:
        e = espnow.ESPNow()
        e.active(True)
    except:
        
        e.active(True)

    try:
        e.add_peer(HOME_MAC)
        e.add_peer(PORTABLE_MAC)
    except:
       
        pass
    
    


# ===== Sync Time =====

def sync_time():

    # 1. Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Niza", "Ariana1609+")

    # Wait for connection
    print("Connecting to Wi-Fi...")
    timeout = 10
    start_time =  time.time()
    while not wlan.isconnected():
        
        if time.time() - start_time > timeout:
            print("Wi-Fi timemout, Skipping NTP")
            wlan.disconnect()
            wlan.active(False)
            return False
        
        time.sleep(1)
    print("Connected! IP:", wlan.ifconfig()[0])


    # 2. Sync with NTP Server
    print("Local time before sync:", time.localtime())
    try:
        # Fetches UTC time and sets the internal RTC
        ntptime.settime() 
        print("NTP sync successful!")
        
        wlan.disconnect()
        wlan.active(False)
        
        return True
    except Exception as e:
        print("Error syncing with NTP:", e)
        
        return False
    
   


     
            
sync_time_state = sync_time()

init_espnow()


# ===== UART =====
# TX = GPIO17
# RX = GPIO16
uart = UART(
    2,
    baudrate=115200,
    tx=17,
    rx=16
)
 
    

def screen_time_func(state):
    
    if state == True:
    # Getting the time
     
        OFFSET_TIME = -6 * 3600
        # Time offset timezone -6 hours
        mexico_seconds = time.time() + OFFSET_TIME # -6 hours in seconds
        mexico_time = time.localtime(mexico_seconds)
        hours, minutes = mexico_time[3], mexico_time[4]
        screen_time = "{:02d}:{:02d}".format(hours, minutes)
        return screen_time
    else:
        
        return "No Time"


# ===== Sensor Setup =====
adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

V_EMPTY = 0.0
V_FULL = 1.41
H_FULL = 1.02

def read_voltage():
    total = 0
    for _ in range(10):
        total += adc.read()
        time.sleep_ms(20)
    raw = total / 10
    return (raw / 4095) * 3.3

def get_height(v):
    return max(0, min((v - V_EMPTY) * (H_FULL / (V_FULL - V_EMPTY)), H_FULL))

def get_percent(h):
    return (h / H_FULL) * 100

def get_liters(h):
    return (h / H_FULL) * 688
    



wdt = WDT(timeout=10000)



time_check = 80
time_check_counter = 0




# ===== Main Loop =====
while True:
    
    v = read_voltage()
    h = get_height(v)
    p = get_percent(h)
    l = get_liters(h)
    st = screen_time_func(sync_time_state)

    # Send as string
    msg = "{:.2f},{:.1f},{:.0f},{:}".format(h, p, l,st)
    
    # UART message
    uart_msg = "{:.2f},{:.1f},{:.2f}".format(h, p,v)
    uart.write(uart_msg)
    
    # Portable ESPNOW message
    portable_msg = "{:.2f},{:.1f},{:.2f}".format(h, p,v)
    
    try:
        e.send(HOME_MAC, msg)
        e.send(PORTABLE_MAC,portable_msg )
    except:
        init_espnow()

    print("Sent:", msg)
    
    time_check_counter = time_check_counter + 1
    
    if time_check_counter > time_check :
       
        wifi_connected_counter = 1
           
        time_check_counter = 0
           
        try:
              
                result = sync_time()
                sync_time_state = result 
                init_espnow()
                
                
        
        except :
        
                sync_time_state = False
                
                init_espnow()
                
    
   

        
        
    
    wdt.feed()
    wifi_connected_counter = 0 
    time.sleep(2)

