# Raspberry-Pi-Pico
# GPS Data Logger

GPS Data Logger is a Python project that reads and parses NMEA sentences from a GPS module. It displays real-time GPS information, including latitude, longitude, satellites, time, speed, heading, and velocity on an OLED display and prints the data to the console.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation

Before running the project, make sure you have the required hardware components and libraries installed:

1. **Hardware**:
   - Raspberry Pi or a compatible microcontroller with I2C and UART interfaces
   - SSD1306 OLED display
   - GPS module compatible with NMEA sentences

2. **Python Libraries**:
   - Install the required Python libraries using pip:

   ```bash
   pip install machine ssd1306 utime
## Usage
    - Connect the SSD1306 OLED display and GPS module to your microcontroller according to the wiring instructions.
    - Run the code on your microcontroller.
    - The OLED display will show GPS data, including latitude, longitude, satellites, time, speed, heading, and velocity (if available).
    - The GPS data is also printed to the console.

## Configuration
You can configure the UART and I2C settings in the code to match your specific hardware connections. Additionally, if your GPS module outputs different NMEA sentences, you may need to modify the code to handle them.

