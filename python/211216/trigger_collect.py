import subprocess
# import cli_collect
from datetime import datetime
import RPi.GPIO as GPIO
import sys

buttonPin = 36   # trigger input from pixhawk
 
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # initialize button pin
    
def loop():
    num_collects = 0 # record number of collects
    
    while True:
        if GPIO.input(buttonPin) == GPIO.LOW: # if triggered
            returnCode = subprocess.call("python3 cli_collect.py --help", shell=True)  # run collect
            num_collects += 1
            print('Number of collects = ' + str(num_collects))
            
            if returnCode != 0:
                open(datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + 'error_' + str(returnCode) + '.txt','+x')
                
def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__' :
    setup()
    
    try:
        loop()
    except KeyboardInterrupt: # When Ctrl + C is pressed, execute this
        destroy()