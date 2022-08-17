import RPi.GPIO as GPIO
 
ledPin = 11
buttonPin = 36
 
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)    # initialize LED pin
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # initialize button pin
     
def loop():
    while True:
        if GPIO.input(buttonPin)==GPIO.LOW: # if button is pressed
            GPIO.output(ledPin, GPIO.HIGH)  # turn on LED
        else:
            GPIO.output(ledPin, GPIO.LOW)   # turn off LED
             
def destroy():
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()
     
if __name__ == '__main__' :
    setup()
    try:
        loop()
    except KeyboardInterrupt: # When Ctrl + C is pressed, execute this
        destroy()
