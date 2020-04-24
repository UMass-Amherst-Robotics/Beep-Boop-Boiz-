import RPi.GPIO as gpio
import time
TRIG = 23
ECHO = 24

def init_sonar():
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG, gpio.OUT)
    gpio.setup(ECHO, gpio.IN)
    gpio.output(TRIG, False)
    time.sleep(1)

def init_motor():
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def forward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def backwards(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def veer_right_forward(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def veer_right_backward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def veer_left_forward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def pivot_right(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def pivot_left(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def get_distance():
    init_sonar()
    gpio.output(TRIG, True)
    time.sleep(0.00001)
    gpio.output(TRIG, False)
    # initializing variables
    pulse_start = 0
    pulse_end = 0
    while gpio.input(ECHO) == 0:
        pulse_start = time.time()
    while gpio.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150
    distance_cm = round(distance_cm, 2)
    gpio.cleanup()
    return distance_cm

def test():
    while 1:
        direction = raw_input("What direction do you want to go?\n")
        if direction == 'forward':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(get_distance())
            forward(tf)
            time.sleep(5)
            end_distance = get_distance()
            print(get_distance())
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'back':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(get_distance())
            backwards(tf)
            time.sleep(5)
            end_distance = get_distance()
            print(get_distance())
            distance_moved = end_distance - start_distance
            print(distance_moved)


def main():
    state = "approachingWall"
    while True:
        if state == "approachingWall":
            distance_from_wall = get_distance()
            if distance_from_wall > 50:
                forward(30)  # change argument to time value that moves you 30 cm
            elif 30 < distance_from_wall <= 50:
                forward(20) # change argument to time value that moves you 20 cm
            elif 15 < distance_from_wall <= 30:
                forward(10) # change argument to time value that moves you 20 cm
            elif 7.5 < distance_from_wall <= 15:
                forward(5) # change argument to time value that moves you 20 cm
            else:
                state = "seekingCorner"
        elif state == "seekingCorner":
            pivot_left(someDistance)
            leftValue = get_distance()
            pivot_right(2 * someDistance)
            rightValue = get_distance()
            if leftValue > rightValue:
                pivot_left(2 * someDistance)
                oldDistance = get_distance()
                while True:
                    pivot_left(smallDistance)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingLeft"
                        break
                    oldDistance = newDistance
            else:
                oldDistance = get_distance()
                while True:
                    pivot_right(smallDistance)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingRight"
                        break
                        oldDistance = newDistance
        elif state == "cornerFoundMovingLeft":
            oldDistance = get_distance()
            while True:
                pivot_left(smallDistance)
                newDistance = get_distance()
                if newDistance > oldDistance:
                    state = "approachingWall"  # possibly move backwards like half the distance we have been incrementing by to perfect positioning?
                    break
                oldDistance = newDistance
        elif state == "cornerFoundMovingRight":
            oldDistance = get_distance()
            while True:
                pivot_right(smallDistance)
                newDistance = get_distance()
                if newDistance > oldDistance:
                    state = "approachingWall"  # possibly move backwards like half the distance we have been incrementing by to perfect positioning?
                    break
                oldDistance = newDistance
test()






