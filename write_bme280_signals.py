import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import smbus2
import bme280
import time
from datetime import datetime

# Influx config
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")
bucket = os.environ.get("INFLUXDB_BUCKET")

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# reading signals from BME280 sensor
ADDRESS = 0x76
bus = smbus2.SMBus(1)
calibration_params = bme280.load_calibration_params(bus, ADDRESS)

data = bme280.sample(bus, ADDRESS, calibration_params)
t = round(data.temperature, 2)
rh = round(data.humidity, 2)
p = round(data.pressure, 2)

point = (
    Point("bme280_signals")
    .tag("location", "office")
    .field("temperature", t)
    .field("humidity", rh)
    .field("pressure", p)
)

write_api.write(bucket=bucket, org=org, record=point)
print(f"[{datetime.now().isoformat()}] temp: {t}°C, humidity: {rh}%, pressure: {p}hPa")
