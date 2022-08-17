import subprocess
# import cli_collect
import time
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import sys

def loop():
    while True:
        # if GPIO.input(buttonPin) == GPIO.LOW: # if triggered
        # returnCode = subprocess.call("python3 cli_collect.py --help", shell=True)  # run collect
        print(time.time())
        #    new_start_time = time.time()
        sleep(1)
        #    elapsed_time = round((new_start_time - old_start_time),2)
        #    print('elapsed time between triggers in seconds: ' + str(elapsed_time))
        #    old_start_time = new_start_time

            # if returnCode != 0:
            #     open(datetime.now().strftime('%Y%m%d_%H%M%S') + '_' + 'error_' + str(returnCode) + '.txt','+x')
                
def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__' :
    try:
        loop()
    except KeyboardInterrupt: # When Ctrl + C is pressed, execute this
        destroy()
