import random
import string
from datetime import datetime

def get_random_hostname():
    prefix = 'DESKTOP-'
    suffix = '.home'
    rand_letters = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return prefix + rand_letters + suffix

def get_random_lat():
    min_lat, max_lat = -90.0, 90.0
    lat = round(random.uniform(min_lat, max_lat), 2)
    return (str(lat))


def get_random_lon():
    min_lon, max_lon = -180.0, 180.0
    lon = round(random.uniform(min_lon, max_lon), 2)
    return str(lon)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_random_sleep():
    min_sleep, max_sleep = 3, 10
    return random.randint(min_sleep, max_sleep)

def get_random_phone_num():
    prefix = '+38599'
    rand_digits = ''.join(random.choices(string.digits, k=7))
    return prefix + rand_digits

def get_alerts_endpoint():
    return "http://localhost:6500/alerts"
