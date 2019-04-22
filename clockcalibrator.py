import RPi.GPIO as GPIO
import time

def step(steps, stepPins):
    stepCounter = 0
    Seq = [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]
    #Seq=Seq[::-1]

    WaitTime = 0.001
    
    while stepCounter < steps:
        stepCounter += 1
        for step in Seq:
            GPIO.output(stepPins[3], step[3])
            GPIO.output(stepPins[2], step[2])
            GPIO.output(stepPins[1], step[1])
            GPIO.output(stepPins[0], step[0])
            time.sleep(WaitTime)
            GPIO.output(stepPins[0], False)
            GPIO.output(stepPins[1], False)
            GPIO.output(stepPins[2], False)
            GPIO.output(stepPins[3], False)    
        print("Step ",stepCounter)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
stepPins = [17,22,23,24]
for pin in stepPins:
    print("Step pins",pin)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, False)
        
done = 'n'
while done == 'n':
    steps = int(input("How many steps? "))
    step(steps, stepPins)
    done = input("All done (y or n)? ")
                  
