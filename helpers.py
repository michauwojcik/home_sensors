
import network
import time
import urequests
from machine import RTC, Pin
from secrets import (
    WIFI_PASSWORD,
    WIFI_SSID,
    INFLUXDB_TOKEN,
    INFLUXDB_ORG,
    INFLUXDB_HOST,
    INFLUXDB_PORT,
    INFLUXDB_BUCKET
)


DAYS = {
    'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6
}
MONTHS = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}


def connect_to_wifi():
    """Connects to the specified Wi-Fi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print('.', end='')
            time.sleep(1)
        
        if wlan.isconnected():
            print('\nConnected! IP:', wlan.ifconfig()[0])
            return wlan
        else:
            print('\nFailed to connect to Wi-Fi.')
            return None
    return wlan


def get_and_set_time():
    """
    Makes a HEAD request to google.com, extracts the Date header, 
    and sets the Pico's RTC.
    """
    try:
        # Use HEAD method for efficiency, only getting headers
        r = urequests.head("https://www.google.com")
        
        # Check if the 'Date' header exists
        if 'Date' not in r.headers:
            print("Error: 'Date' header not found in response.")
            r.close()
            return False

        # Example Header Format: 'Date: Tue, 09 Dec 2025 16:40:24 GMT'
        date_header = r.headers['Date']
        r.close() # Close the connection immediately

        # Split the string: ['Tue,', '09', 'Dec', '2025', '16:40:24', 'GMT']
        parts = date_header.split()

        # Extract components
        day = int(parts[1])
        month = MONTHS[parts[2]]
        year = int(parts[3])
        
        # Time is HH:MM:SS
        time_parts = parts[4].split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2])
        
        # Weekday (0=Mon, 6=Sun). parts[0] is 'Tue,' so we strip the comma.
        weekday = DAYS[parts[0].strip(',')]

        # The date_header time is always UTC (GMT), so the offset is 0.
        
        # Construct the final RTC tuple:
        # (year, month, day, weekday, hour, minute, second, subseconds)
        rtc_tuple = (year, month, day, weekday, hour, minute, second, 0)
        
        # Set the RTC
        rtc = RTC()
        rtc.datetime(rtc_tuple)
        

        ts = f"{rtc_tuple[0]:04d}-{rtc_tuple[1]:02d}-{rtc_tuple[2]:02d} {rtc_tuple[4]:02d}:{rtc_tuple[5]:02d}:{rtc_tuple[6]:02d}"

        return ts

    except Exception as e:
        print(f"An error occurred while fetching time: {e}")
        return False


def write_to_influxdb(line_data):
    """Sends the Line Protocol data to the InfluxDB API."""
    if not line_data:
        print("No data to send.")
        return

    # 🛑 FIX: Manually construct the URL with query parameters.
    # We remove the 'params' keyword argument from urequests.post()
    
    # 1. Base URL for InfluxDB 2.x Write API
    base_url = f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}/api/v2/write"
    
    # 2. Construct the URL Query String manually
    # Precision is set to 's' (seconds), as the Pico typically uses seconds resolution.
    url = f"{base_url}?org={INFLUXDB_ORG}&bucket={INFLUXDB_BUCKET}&precision=s"

    # HTTP Headers for Authentication and Content Type
    headers = {
        'Authorization': f'Token {INFLUXDB_TOKEN}',
        'Content-Type': 'text/plain; charset=utf-8',
        # 'Accept': 'application/json' # Removed as it's often not necessary for urequests
    }

    try:
        print(f"Sending data to Influx on {INFLUXDB_HOST}:{INFLUXDB_PORT}...")
        
        # NOTE: The 'params' argument is REMOVED from the post call!
        response = urequests.post(
            url, 
            headers=headers, 
            data=line_data # The line_data (body) is the Line Protocol string
        )
        
        # InfluxDB returns 204 No Content for a successful write
        if response.status_code == 204:
            print("✅ Data successfully written to InfluxDB.")
        else:
            print(f"❌ InfluxDB Write Failed. Status Code: {response.status_code}")
            # Try to print the error body if available
            try:
                print("Error Body:", response.text)
            except:
                pass
        
        response.close()
    
    except Exception as e:
        # Check for network or DNS issues
        print(f"HTTP Request Error: {e}")

def flash_led(led_pin, on_time=0.5, flashes=1, off_time=0.2):
    """Flashes the onboard LED a specified number of times."""
    for _ in range(flashes):
        led_pin.value(1)  # Turn LED on
        time.sleep(on_time)
        led_pin.value(0)  # Turn LED off
        if flashes > 1:
            time.sleep(off_time)