import subprocess
# import cli_collect
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import sys

buttonPin = 36   # trigger input from pixhawk

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # initialize button pin

def loop():
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW: # if triggered
            returnCode = subprocess.call("python3 cli_collect.py --frequency 121500000 --num_buffers 280", shell=True)  # run collect

            if returnCode != 0:
                open(datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + 'error_' + str(returnCode) + '.txt','+x')
                print('Oopsie there were errors.')

            if returnCode == 0:
                print('Done! No errors.')
            sys.exit()
def destroy():
    GPIO.cleanup()

if __name__ == '__main__' :
    setup()

    try:
        loop()
    except KeyboardInterrupt: # When Ctrl + C is pressed, execute this
        destroy()
