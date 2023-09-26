from machine import Pin, UART, I2C
from ssd1306 import SSD1306_I2C
import utime, time

# Initialize I2C and OLED display
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Initialize GPS UART module
gpsModule = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Global variables
FIX_STATUS = False
TIMEOUT = False
latitude = ""
longitude = ""
satellites = ""
GPStime = ""
speed = 0.0  # Speed in knots (RMC)
heading = 0.0  # Heading in degrees (RMC)
velocity = 0.0  # Ground speed in km/h (VTG)

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime, speed, heading, velocity

    # Set a timeout for GPS data retrieval
    timeout = time.time() + 8

    while True:
        # Read a line from the GPS module
        raw_data = gpsModule.readline()
        
        # Convert bytes to a string and split it
        data = str(raw_data).split(',')

        if data[0] in ["b'$GNGGA", "b'$GPGGA"] and len(data) == 15:
            if all(data[1:8]):
                latitude = convertToDegree(data[2], data[3])
                longitude = convertToDegree(data[4], data[5])
                satellites = data[7]
                GPStime = f"{data[1][0:2]}:{data[1][2:4]}:{data[1][4:6]}"
                FIX_STATUS = True

        elif data[0] == "b'$GNRMC" and len(data) >= 12:
            if all(data[1:10]):
                latitude = convertToDegree(data[3], data[4])
                longitude = convertToDegree(data[5], data[6])
                GPStime = f"{data[1][0:2]}:{data[1][2:4]}:{data[1][4:6]}"
                speed = float(data[7])  # Speed in knots
                heading = float(data[8])  # Heading in degrees
                FIX_STATUS = True

        elif data[0] == "b'$GNVTG" and len(data) >= 10:
            if all(data[1:6]):
                velocity = float(data[7])  # Ground speed in km/h
                heading = float(data[1])  # True heading in degrees
                FIX_STATUS = True

        if time.time() > timeout:
            TIMEOUT = True

        if FIX_STATUS:
            break

def convertToDegree(RawDegrees, direction):
    RawAsFloat = float(RawDegrees)
    first_digits = int(RawAsFloat / 100) 
    next_two_digits = RawAsFloat - float(first_digits * 100) 
    
    converted = float(first_digits + next_two_digits / 60.0)
    
    if direction in ['S', 'W']:
        converted = -converted

    return '{0:.6f}'.format(converted)

while True:
    getGPS(gpsModule)
    
    if FIX_STATUS:
        print("Printing GPS data...")
        print(" ")
        print("Latitude: " + latitude)
        print("Longitude: " + longitude)
        print("Satellites: " + satellites)
        print("Time: " + GPStime)
        print("Speed: {:.2f} knots".format(speed))
        print("Heading: {:.2f} degrees".format(heading))
        print("Velocity: {:.2f} km/h".format(velocity))
        print("----------------------")
        
        oled.fill(0)
        oled.text("GPS LOCATION",0,0)
        oled.text("Latitude: " + latitude,0,20)
        oled.text("Longitude: " + longitude,0,30)
        oled.show()
        
        FIX_STATUS = False

    if TIMEOUT:
        print("No GPS data is found.")
        
        oled.fill(0)
        oled.text("No data found", 0, 0)
        oled.show()
        
        TIMEOUT = False

