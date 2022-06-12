# Import the 2 defined pumps
from Pumping import pumpRight
# Import the defined cooler block
from Cooling import cooler
# Import the reading of temp
from TempSensor import tempsens
# Import the OLED screen
from OLED import oledScreen
# Import the PID controller
from PID import PIDControl
# Import PWM
from PWMPump import pumpLeft
# Import time
import time


#PID controller section
PID = PIDControl(tempsens.read_temp())
#Set the PID controller parameters
PID.setProportional(6)
PID.setIntegral(0.2)
PID.setDerivative(0)
#12500
#Logging section
logFile = open("Data.txt", "w")
logFile.write("Time,Temp\n")
logFile.close()

# Start with high cooling power
cooler.peltHighPower()
cooler.fanOn()

# Function to adjust the speed of the pump 
#according to the actuator
def adjustSpeed(ut):
    if ut <= 2:
        cooler.peltLowPower()
        pumpLeft.speed(0)
    
    elif ut <= 20:
        cooler.peltLowPower()
        pumpLeft.speed(int(275*ut))
        
    else:
        cooler.peltHighPower()
        current = pumpLeft.pwm.freq()
        for i in range((12500-current)//1000):
            time.sleep(0.05)
            pumpLeft.speed(int(current+i*1000))

# Main loop
PIDC = True
# Store a time index variable
timeInd = 0 
while(True):
    newTemp = tempsens.read_temp()
    #Write the new temperature to the log file
    logFile = open("Data.txt", "a")
    logFile.write(str(timeInd)) + "," + str(newTemp) + "\n")
    logFile.close()
    #Update the oled screen
    oledScreen.setTemp(newTemp)
    oledScreen.printOverview()

    #PID controller
    actuatorValue = -PID.update(newTemp)
    print("Actuator:" + str(actuatorValue))
    print("Time:" + str(timeInd))
    print("PID Values:" + PID.overview)
    timeInd += 10
    
    if PIDC == True:
        adjustSpeed(actuatorValue)
    time.sleep(10)
    # Run for specific number of seconds
    if timeInd > 600:
        break

