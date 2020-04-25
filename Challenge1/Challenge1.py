# Beep-Boop-Boiz
# UMass Robotics - Challenge 1
# Presented on April 25, 2020


import RPi.GPIO as gpio
import time

# global variables for ultrasonic sensor that should be able to be implemented to native functions
TRIG = 23
ECHO = 24

# Initializes sonar sensor, to be used as setup for our get_distance() function
def init_sonar():
    gpio.setmode(gpio.BCM)
    gpio.setup(TRIG, gpio.OUT)
    gpio.setup(ECHO, gpio.IN)
    gpio.output(TRIG, False)
    time.sleep(1)

# Initializes motors as output pins, to be used as setup for our motion functions
def init_motor():
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

# Moves all four wheels forward for a specified time-frame, tf
def forward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

# Moves all four wheels backwards for a specified time-frame, tf
def backwards(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

# Veers the robot in a slight arc to the right, moving forward for a specified time-frame, tf
# Not used in this code, but may have other practical applications
def veer_right_forward(tf):
    init_motor()
    gpio.output(7, True)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

# Veers the robot in a slight arc to the right, moving backwards for a specified time-frame, tf
# Not used in this code, but may have other practical applications
def veer_right_backward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

# Veers the robot in a slight arc to the left, moving forward for a specified time-frame, tf
# Not used in this code, but may have other practical applications
def veer_left_forward(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

# Moves the left wheels forward and the right wheels backwards for a specified time-frame, tf
# Results in a concise pivoting motion
def pivot_left(tf):
    init_motor()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

# Moves the right wheels forward and the left wheels backwards for a specified time-frame, tf
# Results in a concise pivoting motion
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
    for i in range(0,10):  # for loop that averaged recorded distances to increase accuracy of our measurement from the ultrasonic sensor
        gpio.output(TRIG, True)
        time.sleep(0.00001)  # sensor requires a 10 us pulse to trigger module
        gpio.output(TRIG, False)
        # initializing variables
        pulse_start = 0  # initializing start and end variables
        pulse_end = 0
        while gpio.input(ECHO) == 0:
            pulse_start = time.time()  # start time is recorded
        while gpio.input(ECHO) == 1:
            pulse_end = time.time()  # end time is recorded
        pulse_duration = pulse_end - pulse_start  # pulse duration is calculated
        distance_cm = pulse_duration * 17150  # distance is converted to cm and rounded
        distance_cm = round(distance_cm, 2)
        current_sum_dist += distance_cm  # distances are added to sum

    final_distance = current_sum_dist/10  # average is calculated
    gpio.cleanup()
    return final_distance

# function that allowed us to situate the robot in a suitable location for testing
def test():
    while 1:
        direction = raw_input("What direction do you want to go?\n")
        if direction == 'forward':  # allows us to move the robot forward for a time-frame of our choice, just input "forward"
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            forward(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'back':  # allows us to move the robot backwards for a time-frame of our choice, just input "back"
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            backwards(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'PL':  # allows us to pivot the robot to the left for a time-frame of our choice, just input "PL"
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            pivot_left(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)
        if direction == 'PR':  # allows us to pivot the robot to the right for a time-frame of our choice, just input "PR"
            tf = input("How many seconds? \n")
            start_distance = get_distance()
            print(start_distance)
            pivot_right(tf)
            time.sleep(2)
            end_distance = get_distance()
            print(end_distance)
            distance_moved = end_distance - start_distance
            print(distance_moved)

        # NOTE, start, end, and total distance travelled are printed for each of the above test functions

# main code to be executed for challenge 1
def main():
    state = "approachingWall"  # initial state is when the robot is approaching the wall, theoretically from any angle
    status = ''  # possible status variable that we decided not to implement
    while True:

        # if the robot is approaching the wall, it will get closer and closer by traveling shorter distances until it passes a threshold value
        if state == "approachingWall":
            newDistance = get_distance()
            print(get_distance())
            if newDistance > 60:
                forward(.5)  # moves robot a "long" distance
                time.sleep(1)
                oldDistance = newDistance
                newDistance = get_distance()
                if abs(newDistance - oldDistance) < 2:
                    backwards(.2)  # case where robot gets stuck approaching a wall and fixes itself
                    pivot_right(.25)
            elif 35 < newDistance <= 60:
                forward(.125)  # moves robot a "short" distance
                time.sleep(1)
                oldDistance = newDistance
                newDistance = get_distance()
                if abs(newDistance - oldDistance) < 2:  # case where robot gets stuck approaching a wall and fixes itself
                    backwards(.2)
                    pivot_right(.25)
            else:  # once threshold is broken and robot is close enough to the perimeter, state changes
                state = "seekingCorner"
                print(state)


        # if the robot is seeking a corner, samples are taken continuously until we find a point of maximum distance
        elif state == "seekingCorner":
            # after robot is close to wall, one distance sample is taken from the left, and one is taken from the right
            # robot will start seeking corner for whatever the greater distance value is, since that is the side that
            # should be closer to the corner
            pivot_left(.25)
            leftValue = get_distance()
            pivot_right(.5)
            rightValue = get_distance()

            if leftValue > rightValue:  # if value to the left is greater
                pivot_left(.5)  # robot pivots back to the left to make up for when it pivoted right in the above check
                oldDistance = get_distance()
                # robot will continue pivoting left until newDistance is less than oldDistance, which means we have
                # finally passed a corner
                while True:
                    pivot_left(.22)
                    time.sleep(1)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingLeft"
                        #status = 'Left'
                        print(state)
                        break
                    oldDistance = newDistance  # oldDistance becomes previous newDistance value

            else:  # if value to the right is greater
                oldDistance = get_distance()
                # robot will continue pivoting right until newDistance is less than oldDistance, which means we have
                # finally passed a corner
                while True:
                    pivot_right(.22)
                    time.sleep(1)
                    newDistance = get_distance()
                    if newDistance < oldDistance:
                        state = "cornerFoundMovingRight"
                       # status = 'Right'
                        print(state)
                        break
                    oldDistance = newDistance  # oldDistance becomes previous newDistance value

        # this state essentially does the same thing as "seekingCorner", turning in the same direction continuously,
        # but this time the robot is looking for a minimum value, which means we have found a point of perpendicularity
        # with the wall
        elif state == "cornerFoundMovingLeft":
            oldDistance = get_distance()
            while True:
                # turns at smaller angles for greater distances from the wall, as there is a higher risk of setting
                # ourselves up not perpendicular
                if oldDistance > 100:
                    time_value = .215
                # turns at larger angles for smaller distances, to increase efficiency
                else:
                    time_value = .25
                pivot_left(time_value)  # continues to pivot left
                time.sleep(1)
                newDistance = get_distance()
                print(newDistance)

                # possible correction implementation for long distances, decided not to use

              #  if newDistance > oldDistance and newDistance > 80:
               #     state = "approachingWall"
               #     high_int_val = oldDistance + 1
               #     while newDistance > high_int_val:
                #        newDistance = get_distance()
                #        pivot_left(.075)
                #    print(state)
                #    return  # is return now, change back to break after test

                if newDistance > oldDistance:  # while loop breaks once perpendicularity is found
                    state = "approachingWall"
                    print(state)
                    break
                oldDistance = newDistance  # oldDistance becomes previous newDistance value

        # this state essentially does the same thing as "seekingCorner", turning in the same direction continuously,
        # but this time the robot is looking for a minimum value, which means we have found a point of perpendicularity
        # with the wall
        elif state == "cornerFoundMovingRight":
            oldDistance = get_distance()
            while True:
                # turns at smaller angles for greater distances from the wall, as there is a higher risk of setting
                # ourselves up not perpendicular
                if oldDistance > 100:
                    time_value = .215
                # turns at larger angles for smaller distances, to increase efficiency
                else:
                    time_value = .25
                pivot_right(time_value)
                time.sleep(1)
                newDistance = get_distance()
                print(newDistance)

                # possible correction implementation for long distances, decided not to use

                #if newDistance > oldDistance and newDistance > 80:
                #    state = "approachingWall"
                #    high_int_val = oldDistance + 1
                #    while newDistance > high_int_val:
                #        newDistance = get_distance()
                #        pivot_left(.075)
                #    print(state)
                #    return  # is return now, change back to break after test

                if newDistance > oldDistance:  # while loop breaks once perpendicularity is found
                    state = "approachingWall"
                    print(state)
                    break

                oldDistance = newDistance  # oldDistance becomes previous newDistance value

                # where we would have implemented the status variable, essentially, if a corner was found moving to the
                # left, the status would have told the program to continue turning to the left, and the opposite would
                # occur if the corner was found moving to the right
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

# function that allows us to choose what we want to run
def choice():
    choice = raw_input("what function would you like to run\n")
    if choice == 'test':
        test()
    if choice == 'main':
        main()


choice()






