import time
import RPi.GPIO as GPIO
import timeit
import datetime

def gettime():

    now = datetime.datetime.now().time()
    print("The time is",now)
    breakfast = [datetime.time(7,30),datetime.time(7,59)]
    school = [datetime.time(8,00),datetime.time(8,30)]
    lunch = [datetime.time(11,30),datetime.time(12,30)]
    quiet = [datetime.time(12,30),datetime.time(14,00)]
    dinner = [datetime.time(17,30),datetime.time(18,30)]
    cleaning = [datetime.time(19,00),datetime.time(19,29)]
    bedtime = [datetime.time(19,30),datetime.time(6,00)]

    times = {"breakfast":breakfast, "school":school, "lunch":lunch,
             "quiet":quiet, "dinner":dinner, "cleaning":cleaning,
             "bedtime":bedtime}

    for time in times:
        if time == "bedtime":
            if now >= times[time][0] or now <= times[time][1]:
                return time
        elif times[time][0] <= now <= times[time][1]:
            return time
    return 'play'


def getsteps(currenttime):

    with open('clocklocation.txt','r') as file:
        clocktime = file.read()

    locations = ['play','breakfast','school','lunch','quiet','dinner','cleaning',
                 'bedtime']

    clocklocation = [i for i, x in enumerate(locations) if x == clocktime][0]
    
    if currenttime == clocktime:
        steps = 0
        
    elif currenttime == 'play':
        steps = 512 - (clocklocation*64)        

    else:
        newclocklocation = [i for i, x in enumerate(locations) if x == currenttime][0]
        steps = (newclocklocation - clocklocation)*64

    return steps, clocktime

def turnclock(steps, newclocklocation, stepPins):
    print(steps)
    Seq = [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]
    #Seq=Seq[::-1]

    WaitTime = 0.002

    stepCounter = 0
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
    with open('clocklocation.txt','w') as file:
        file.write(newclocklocation)

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    stepPins = [17,22,23,24]
    for pin in stepPins:
        print("Step pins",pin)
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, False)

    while True:
        activity = gettime()
        distance, clockactivity = getsteps(activity)
        print(distance)
        if distance > 0 and activity != clockactivity:
            print("Moving the clock from",clockactivity,"to",activity)
            turnclock(distance, activity, stepPins)
        else:
            print("Clock is already set at",activity)
        time.sleep(59)


if __name__ == "__main__":
    main()
