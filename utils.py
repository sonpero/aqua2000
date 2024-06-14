import subprocess
import json
from datetime import datetime


def mount_nas():
    # Define the bash command
    bash_command = "sudo mount -t nfs 192.168.1.9:/volume1/aqua2000 /aqua2000"

    # Launch the command using subprocess
    process = subprocess.Popen(bash_command.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    # Wait for the process to terminate
    output, error = process.communicate()

    # Check if there's any output
    if output:
        print("Output:", output.decode())
    if error:
        print("Error:", error.decode())


def define_the_path(sensor_name):
        # Specify the file path
    date_now = datetime.now().strftime("%Y_%m_%d")
    year = datetime.now().strftime("%Y")
    path = f"/aqua2000/{year}/{sensor_name}_{date_now}.json"
    return path


def read_json(sensor):
    """
    read the json file if exist, if note create one
    """
    path = define_the_path(sensor_name=sensor)
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
        data = {
   "sensor_name": sensor,
   "measurements": []
    }    
    return data


def write_json(sensor_name, value):
    """
    write the json file 
    """
    mypath = define_the_path(sensor_name=sensor_name)

    # Write the data to the JSON file
    with open(mypath, 'w') as json_file:
        json.dump(value, json_file, indent=4)

    print(f"sensor JSON file has been created at: {mypath}")
