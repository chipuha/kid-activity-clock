"""
This code uses a raspberry pi B to control a 28BYJ-48 stepper motor paired with
the ULN2003 driver board.

The goal is to control a child's activity clock which points to scheduled
activities like a clock would point to the time.

"""

import time
import datetime
import RPi.GPIO as GPIO


def get_time():
    """
    Retrieves current time and compares it to a schedule.  Returns the activity
    according to the schedule.
    """
    now = datetime.datetime.now().time()
    print("The time is", now)
    breakfast = [datetime.time(7, 30), datetime.time(7, 59)]
    school = [datetime.time(8, 00), datetime.time(8, 30)]
    lunch = [datetime.time(11, 30), datetime.time(12, 30)]
    quiet = [datetime.time(12, 30), datetime.time(14, 00)]
    dinner = [datetime.time(17, 30), datetime.time(18, 30)]
    cleaning = [datetime.time(19, 00), datetime.time(19, 29)]
    bedtime = [datetime.time(19, 30), datetime.time(6, 00)]

    schedule = {"breakfast":breakfast, "school":school, "lunch":lunch,
                "quiet":quiet, "dinner":dinner, "cleaning":cleaning,
                "bedtime":bedtime}

    for activity in schedule:
        if activity == "bedtime":
            if now >= schedule[activity][0] or now <= schedule[activity][1]:
                return activity
        elif schedule[activity][0] <= now <= schedule[activity][1]:
            return activity
    return 'play'


def get_steps(current_time):
    """
    Compares the activty the clock is currently set at to the scheduled
    activity and calculates the number of steps the stepper motor needs to
    perform to point at the new activity
    """
    with open('clock_location.txt', 'r') as file:
        clock_time = file.read()

    locations = ['play', 'breakfast', 'school', 'lunch', 'quiet', 'dinner',
                 'cleaning', 'bedtime']

    clock_location = [i for i, x in enumerate(locations) if x == clock_time][0]

    if current_time == clock_time:
        steps = 0

    elif current_time == 'play':
        steps = 512 - (clock_location * 64)

    else:
        new_clock_location = [i for i, x in enumerate(locations) if x == current_time][0]
        steps = (new_clock_location - clock_location) * 64

    return steps, clock_time

def turn_clock(steps, new_clock_location, pins):
    """
    Once the number of steps has been calculated by get_steps() this function
    turns to clock the inputed number of steps
    """
    print(steps)
    step_sequence = [[1, 0, 0, 1],
                     [1, 0, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 0, 1, 0],
                     [0, 0, 1, 1],
                     [0, 0, 0, 1]]
    #step_sequence=step_sequence[::-1]

    wait_time = 0.002

    step_counter = 0
    while step_counter < steps:
        step_counter += 1
        for step in step_sequence:
            GPIO.output(pins[3], step[3])
            GPIO.output(pins[2], step[2])
            GPIO.output(pins[1], step[1])
            GPIO.output(pins[0], step[0])
            time.sleep(wait_time)
            GPIO.output(pins[0], False)
            GPIO.output(pins[1], False)
            GPIO.output(pins[2], False)
            GPIO.output(pins[3], False)
    with open('clock_location.txt', 'w') as file:
        file.write(new_clock_location)

def main():
    """
    Main function controling the clock
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pins = [17, 22, 23, 24]
    for pin in pins:
        print("Step pins", pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    while True:
        activity = get_time()
        distance, clock_location = get_steps(activity)
        print(distance)
        if distance > 0 and activity != clock_location:
            print("Moving the clock from", clock_location, "to", activity)
            turn_clock(distance, activity, pins)
        else:
            print("Clock is already set at", activity)
        time.sleep(59)


if __name__ == "__main__":
    main()
