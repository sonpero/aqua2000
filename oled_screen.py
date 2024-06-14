from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=2)

# Box and text rendered in portrait mode
with canvas(device) as draw:
    # draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.rectangle((10, 10, 30, 30), outline="white", fill="red")
    draw.text((10, 0), "Hello World", fill="red")
sleep(30)