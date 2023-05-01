import random
import string
from datetime import datetime

def get_random_hostname():
    prefix = 'DESKTOP-'
    suffix = '.home'
    rand_letters = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return prefix + rand_letters + suffix

def get_random_fer_lat_lon():
    bounds = [[45.80006, 15.97061], [45.80163, 15.97181]]
    coordinates = []
    lat = random.uniform(bounds[0][0], bounds[1][0])
    lng = random.uniform(bounds[0][1], bounds[1][1])
    coordinates.append(str(lat))
    coordinates.append(str(lng))
    return coordinates

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
    return "https://fer.westeurope.cloudapp.azure.com/alerts"
