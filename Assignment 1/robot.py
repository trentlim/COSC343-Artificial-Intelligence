#!/usr/bin/env python3

# Wednesday 31 March
# Group 3 - Harry Pittar, Trent Lim, Lachlan Campbell, Shaun Liew

from ev3dev2.led import Leds
from ev3dev2.motor import LargeMotor, OUTPUT_B, OUTPUT_C, MoveTank
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import UltrasonicSensor, ColorSensor
from time import sleep

us = UltrasonicSensor()
cs = ColorSensor()
leds = Leds()
sound = Sound()
drive = MoveTank(OUTPUT_B, OUTPUT_C)
mLeft = LargeMotor(OUTPUT_B)
mRight = LargeMotor(OUTPUT_C)
direction = "north"
location = 0

# Turn right 90 degrees by turning both wheels in opposite direction
# If else statements to change direction variable based on current direction
def turnRight():
    global direction
    drive.on_for_rotations(10, -10, 0.52)
    if direction == "north":
        direction = "east"
    elif direction == "east":
        direction = "south"
    elif direction == "south":
        direction = "west"
    else:
        direction = "north"

# Turn left 90 degrees by turning both wheels in opposite direction
# If else statements to change direction variable based on current direction
def turnLeft():
    global direction
    drive.on_for_rotations(-10, 10, 0.52)
    if direction == "north":
        direction = "west"
    elif direction == "east":
        direction = "north"
    elif direction == "south":
        direction = "east"
    else:
        direction = "south"

# Turns left and drives on until it reaches the left side of the tile
# Returns to original location
# While statement to calculate the the number of wheel rotation increments
#   it takes to get to the other side
# Returns number of rotation increments
def checkLeft():
    sleep(1)
    drive.on_for_rotations(-10, 10, 0.25)
    sleep(0.5)
    counter = 0
    while cs.reflected_light_intensity < 12:
        drive.on_for_rotations(10, 10, 0.05)
        counter +=1
    sleep(0.5)
    drive.on_for_rotations(-10, -10, 0.05*counter)
    sleep(0.5)
    drive.on_for_rotations(10, -10, 0.25)
    sleep(0.5)
    return counter

# Turns right and drives on until it reaches the left side of the tile
# Returns to original location
# While statement to calculate the the number of wheel rotation increments
#   it takes to get to the other side
# Returns number of rotation increments
def checkRight():
    sleep(1)
    drive.on_for_rotations(10, -10, 0.25)
    sleep(0.5)
    counter = 0
    while cs.reflected_light_intensity < 12:
        drive.on_for_rotations(10, 10, 0.05)
        counter +=1
    sleep(0.5)
    drive.on_for_rotations(-10, -10, 0.05*counter)
    sleep(0.5)
    drive.on_for_rotations(-10, 10, 0.25)
    sleep(0.5)
    return counter

# Checks the distance between the robot and both sides of the tile
# If statement to check which side is further away from the robot
# Centers robot by driving towards the further side, taking the difference in 
#   wheel rotaions required to get to each side
def correction():
    sleep(1)
    drive.on_for_rotations(10, 10, 0.1)
    left = checkLeft()
    right = checkRight()
    # If the left side of the tile is further than the right side of the tile,
    # drive towards the left with the difference of rotations required to get
    # to either side (and vice versa)
    if left > right:
        drive.on_for_rotations(-10, 10, 0.25)
        sleep(0.5)
        drive.on_for_rotations(10, 10, (left - right) * 0.05)
        sleep(0.5)
        drive.on_for_rotations(10, -10, 0.25)
    else:
        drive.on_for_rotations(10, -10, 0.25)
        sleep(0.5)
        drive.on_for_rotations(10, 10, (right - left) * 0.05)
        sleep(0.5)
        drive.on_for_rotations(-10, 10, 0.25)

# Function used to move onwards to next black tile
# using the light intensity method from the colour sensor,
# while reporting aloud the location of the robot.
# Incorporates the correction function and direction
# to add the correct number the location counter.
def findNextBlack():
    global location
    if cs.reflected_light_intensity > 12:
        while cs.reflected_light_intensity > 12:
            drive.on(10, 10)
        drive.stop()
        correction()
        sleep(1)
        if direction == "east":
            location += 1
        elif direction == "south":
            location += 15
        elif direction == "north":
            location += 1

        print(location)
        sound.speak(location)
        drive.on_for_rotations(10, 10, 0.23)

        return
    else:
        while cs.reflected_light_intensity < 15:
            drive.on(10, 10)
        drive.stop()
        findNextBlack()

# Function used to sense which row the bottle is on.
# Consists of if else and while statements to check
# the current state of the sensor and drive forward
# or stop accordingly. 
def findTower():
    drive.on_for_rotations(10, 10, 1)
    drive.on_for_rotations(-10, 10, 0.6)
    sleep(1)
    if us.distance_centimeters < 200:
        drive.on_for_rotations(10, -10, 0.1)
        findFinalTile()
        while us.distance_centimeters > 10:
            drive.on(10, 10)
        drive.stop()
    else:
        drive.on_for_rotations(10, -10, 0.6)
        findNextBlack()
        findTower()
        
# The final tile function - consists if elif statements
# to figure out the distance and location of the bottle.
# Uses ultrasonic sensor to find distance of bottle in 
# relation to the last black tile location.
def findFinalTile():
    finalTile = 0
    if us.distance_centimeters < 40:
        if location == 55:
            finalTile = 1
        elif location == 70:
            finalTile = 4
        elif location == 85:
            finalTile = 7
        elif location == 100:
            finalTile = 10
    elif us.distance_centimeters < 70:
        if location == 55:
            finalTile = 2
        elif location == 70:
            finalTile = 5
        elif location == 85:
            finalTile = 8
        elif location == 100:
            finalTile = 11
    elif us.distance_centimeters < 100:
        if location == 55:
            finalTile = 3
        elif location == 70:
            finalTile = 6
        elif location == 85:
            finalTile = 9
        elif location == 100:
            finalTile = 12

    sound.beep()
    sound.speak('Tower is in tile ' + str(finalTile))
    print('Tower is in tile ' + str(finalTile))

# Function which begins the course, then 
# calls appropriate functions needed to complete
# the run. Uses while statements to make right
# hand turns once desired location of the robot
# is satisfied.
def initialize():
    drive.on_for_rotations(10, 10, 0.25)
    findNextBlack()
    sleep(1)
    turnRight()
    sleep(1)
    while location < 10:
        findNextBlack()
    sleep(1)
    turnRight()
    sleep(1)
    while location < 55:
        findNextBlack()
    findTower()

initialize()
