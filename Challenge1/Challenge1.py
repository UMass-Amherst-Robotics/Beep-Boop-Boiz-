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

def pivot_left(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def pivot_right(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def get_distance():
    init_sonar()
    current_sum_dist = 0
    for i in range(0,10):
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
        current_sum_dist += distance_cm

    final_distance = current_sum_dist/10
    gpio.cleanup()
    return final_distance

def test():
    while 1:
        direction = raw_input("What direction do you want to go?\n")
        if direction == 'forward':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            forward(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'back':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            backwards(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'PL':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            pivot_left(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'PR':
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            pivot_right(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)


def main():
    state = "approachingWall"
    status = ''
    while True:
        if state == "approachingWall":
            newDistance = get_distance()
            print(get_distance())
            if newDistance > 60:
                forward(.5)  # change argument to time value that moves you 30 cm
                time.sleep(1)
                oldDistance = newDistance
                newDistance = get_distance()
                if abs(newDistance - oldDistance) < 2:
                    backwards(.2)
                    pivot_right(.25)
            elif 35 < newDistance <= 60:
                forward(.125)  # change argument to time value that moves you 20 cm
                time.sleep(1)
                oldDistance = newDistance
                newDistance = get_distance()
                if abs(newDistance - oldDistance) < 2:
                    backwards(.2)
                    pivot_right(.25)
            else:
                state = "seekingCorner"
                print(state)

        elif state == "seekingCorner":
            pivot_left(.25)
            leftValue = get_distance()
            pivot_right(.5)
            rightValue = get_distance()
            if leftValue > rightValue:
                pivot_left(.5)
                oldDistance = get_distance()
                while True:
                    pivot_left(.22)
                    time.sleep(1)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingLeft"
                        #status = 'Left'
                        print(state)
                        break
                    oldDistance = newDistance
            else:
                oldDistance = get_distance()
                while True:
                    pivot_right(.22)
                    time.sleep(1)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingRight"
                       # status = 'Right'
                        print(state)
                        break
                    oldDistance = newDistance

        elif state == "cornerFoundMovingLeft":
            oldDistance = get_distance()
            while True:
                if oldDistance > 100:
                    time_value = .215
                else:
                    time_value = .25
                pivot_left(time_value)
                time.sleep(1)
                newDistance = get_distance()
                print(newDistance)
              #  if newDistance > oldDistance and newDistance > 80:
               #     state = "approachingWall"
               #     high_int_val = oldDistance + 1
               #     while newDistance > high_int_val:
                #        newDistance = get_distance()
                #        pivot_left(.075)
                #    print(state)
                #    return  # is return now, change back to break after test
                if newDistance > oldDistance:
                    state = "approachingWall"
                    print(state)
                    break  # is return now, change back to break after test
                oldDistance = newDistance

        elif state == "cornerFoundMovingRight":
            oldDistance = get_distance()
            while True:
                if oldDistance > 100:
                    time_value = .215
                else:
                    time_value = .25
                pivot_right(time_value)
                time.sleep(1)
                newDistance = get_distance()
                print(newDistance)
                #if newDistance > oldDistance and newDistance > 80:
                #    state = "approachingWall"
                #    high_int_val = oldDistance + 1
                #    while newDistance > high_int_val:
                #        newDistance = get_distance()
                #        pivot_left(.075)
                #    print(state)
                #    return  # is return now, change back to break after test
                if newDistance > oldDistance:
                    state = "approachingWall"
                    print(state)
                    break  # is return now, change back to break after test

                oldDistance = newDistance
        '''    
                elif state == "seekingCorner" and status == 'Left':
                    oldDistance = get_distance()
                    while True:
                        pivot_left(.25)
                        time.sleep(1)
                        newDistance = get_distance()
                        if newDistance < oldDistance:
                            state = "cornerFoundMovingLeft"
                            print(state)
                            break
                        oldDistance = newDistance

                elif state == "seekingCorner" and status == 'Right':
                    oldDistance = get_distance()
                    while True:
                        pivot_right(.25)
                        time.sleep(1)
                        newDistance = get_distance()
                        if newDistance < oldDistance:
                            state = "cornerFoundMovingRight"
                            print(state)
                            break
                        oldDistance = newDistance
                '''

def choice():
    choice = raw_input("what function would you like to run\n")
    if choice == 'test':
        test()
    if choice == 'main':
        main()


choice()






