# reading signals from BME280 sensor

import time
from datetime import datetime

import bme280
import smbus2

address = 0x76

bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)
t = round(data.temperature, 2)
rh = round(data.humidity, 2)
p = round(data.pressure, 2)

print(f"[{datetime.now().isoformat()}] temp: {t}°C, humidity: {rh}%, pressure: {p}hPa")
