from helpers import get_and_set_time


def get_sensor_data_line_protocol(bme_sensor):
    """Reads BME280 data and formats it into InfluxDB Line Protocol."""

    try:
        t, p, h = bme_sensor.read_compensated_data()
        temp_c = round(t / 100, 2)
        press_hpa = round(p / 256 / 100, 2)
        hum_rh = round(h / 1024, 2)
    except Exception as e:
        print(f"Could not parse data strings: {e}")
        return None

    # The Measurement and Tag Set
    measurement = "bme280_signals"
    tags = "location=kitchen,sensor=bme280"

    # The Field Set (using f-string formatting)
    fields = f"temperature={temp_c},pressure={press_hpa},humidity={hum_rh}"

    # Combine into Line Protocol
    line_protocol = f"{measurement},{tags} {fields}"
    print(
        f"[{get_and_set_time()}] [RPi Pico] "
        f"temperature: {temp_c} °C; pressure: {press_hpa} hPa; humidity: {hum_rh} %"
    )

    return line_protocol
