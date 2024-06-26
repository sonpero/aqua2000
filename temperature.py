import os
import glob
import time

from datetime import datetime

from utils import mount_nas, write_json, read_json

# mount nas partition
mount_nas()

# temperature
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    """
    read the temperature from the sensor
    """
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    """
    return temperature in degres
    """
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_c = round(temp_c,1)
        return temp_c

while True:
    # read the temp
	value = read_temp()
	print(f'Temperature is : {value}')
    # open the json file
	data = read_json('temperature')
	value_to_append = {'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": value}
    #  append the data and write to json
	data['measurements'].append(value_to_append)
	write_json('temperature', data)
	time.sleep(60)

