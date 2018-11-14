import os
import RPi.GPIO as GPIO
from time import sleep

get_sms = os.popen('get_sms').read()
get_sms_split = get_sms.split(">")
get_sms_message = get_sms_split[13].split("<")
get_sms_time = get_sms_split[15].split("<")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

count = 0
if str(get_sms_message) in open('last_sms').read():
    while (count < 4):
        GPIO.output(8, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(8, GPIO.LOW)
        sleep(0.1)
        count += 1
    with open("last_sms", "w") as text_file:
        text_file.write(str(get_sms_message)
else:
    print("nothing to do...")