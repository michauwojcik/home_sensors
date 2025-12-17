"""Run reading signals and writing them to InfluxDB on RPi Pico."""

from time import sleep

import bme280
from machine import I2C, Pin

from helpers import connect_to_wifi, flash_led, write_to_influxdb
from read_bme280_mpy import get_sensor_data_line_protocol

if not connect_to_wifi():
    raise SystemExit("Cannot proceed without Wi-Fi connection.")

i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400_000)
bme = bme280.BME280(i2c=i2c, address=0x76)

led = Pin("LED", Pin.OUT)

while True:
    line_data = get_sensor_data_line_protocol(bme)
    write_to_influxdb(line_data)
    flash_led(led)
    sleep(30)
