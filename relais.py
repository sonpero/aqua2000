import RPi.GPIO as gpio
from datetime import datetime, time


def is_current_time_in_slot(start_time: time, end_time: time) -> bool:
    # Get the current time
    current_time = datetime.now().time()

    # Check if the current time is within the start and end time slot
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:  # Over midnight case
        return current_time >= start_time or current_time <= end_time
    

gpio.setmode(gpio.BCM)

# set gpio output
gpio.setup(17, gpio.OUT)

while True:
    # Define the start and end times of the slot (24-hour format)
    start_time = time(14, 0)  # 10:00 PM
    end_time = time(21, 0)    # 6:00 AM
    # Get the boolean result
    is_in_slot = is_current_time_in_slot(start_time, end_time)
    # Print the result
    print(f"Is the current time in the slot? {is_in_slot}")
    if is_in_slot:
        print("on")
        gpio.output(17, gpio.HIGH)
    else:
        print("off")
        gpio.output(17, gpio.LOW)