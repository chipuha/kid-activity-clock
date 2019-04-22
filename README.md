# kid-activity-clock
Control code for a stepper motor used in creating a "clock" pointing to the current activity.

I decided to create this clock after I realized that most of my time as a parent was being used telling my daughter what "time" it was (dinner time, bed time, time to clean, time to be quiet, etc).

I came up with this clock that would just point to the current activity hoping I would be a little more convincing that it was time to do anything.

I used a 28BYJ-48 stepper motor paired with the ULN2003 driver board powered by a raspberry pi B.

You can find the stepper motor and driver board as part of a kit here - https://www.amazon.com/dp/B01CP18J4A/ref=cm_sw_em_r_mt_dp_U_PZqVCb1K9CJ87


clockcalibrator.py - 

Since the stepper motor has no idea what it is truely point at, I run this code periodically when I need to manually adjust what it's pointing at.


clocklocation.txt - 

This stores the clock's current location so even if the code cuts out for some reason, it can pick up right where it left off.


ClockSpin.py - 

The main code.  Every 59 seconds (it takes the raspberry pi a little less than 1 second to run the code) it checks the time against a set schedule (def gettime).  If it needs to update the clock, it calculates the number of steps from where it is to what the new activity is (def getsteps).  It then spins to the clock (def turnclock).
