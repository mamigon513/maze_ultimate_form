######FUNCTIONS######

#magnet checking function
def magnet_detect():
    mag = 0
    magY = input.magnetic_force(Dimension.Y)
    magX = input.magnetic_force(Dimension.X)
    magZ = input.magnetic_force(Dimension.Z)
    # take the distance so you can sense in any direction
    force = Math.pow((magX*magX + magY*magY + magZ*magZ), .5)
    if force >= 500:
        mag = 1
         # turn headlights green
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
    return mag

## BACKGROUND MUSIC FUNCTION ##
def missionImpossibleMusic(bpm):
    music.play(music.string_playable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("C5 C5 G4 G4 - G4 G4 G4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("Fb4 Fb4 F4 F4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("C5 C5 G4 G4 - G4 G4 G4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("Fb4 Fb4 F4 F4", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("A6 G6 D5 D5 D5 D5 D5 D5 - -", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("A6 G6 Db5 Db5 Db5 Db5 Db5 Db5 - -", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("A6 G6 C5 C5 C5 C5 C5 C5 - -", bpm),
        music.PlaybackMode.UNTIL_DONE)
    music.play(music.string_playable("Bb4 C5 - -", bpm),
        music.PlaybackMode.UNTIL_DONE)

# make music play in background
def onIn_background():
    global end
    music.set_volume(100)
    while end  ==  0:
        missionImpossibleMusic(350)
        basic.pause(500)
    pass

## DIRECTION CORRECTION FUNCTIONS ##
def straighten_to_line():
    #keep counter to break while loop
    count = 0
    error = CutebotPro.get_offset()

    # turn on headlights(pink = 247, 25, 236)
    CutebotPro.single_headlights(CutebotProRGBLight.RGBL, 247, 25, 236)
    CutebotPro.single_headlights(CutebotProRGBLight.RGBR, 247, 25, 236)
    #keep turning till we are straight
    while(abs(error) > 0 and count < 15):
        # update count of while loop iterations so we can prevent getting stuck
        count = count + 1
        #get offset
        error = CutebotPro.get_offset()
        # set turn speed
        speed = 50 + (abs(error)/3000)*50
        # turn right
        if error > 0:
            #turn on right headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(CutebotProRGBLight.RGBR, 51, 255, 252)
            CutebotPro.pwm_cruise_control(speed, 0)
            basic.pause(30)
            # turn left
        elif error < 0:
            #turn on left headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(CutebotProRGBLight.RGBL, 51, 255, 252)
            CutebotPro.pwm_cruise_control(speed*-1, 0)
            basic.pause(30)
        # turn off headlights
        CutebotPro.turn_off_all_headlights()
        CutebotPro.pwm_cruise_control(0, 0)
        basic.pause(50)
        error = CutebotPro.get_offset()

def detect_line():
    global magnet_count
    # get the line tracking offset
    error = CutebotPro.get_offset()
    line = 0
    # detects black line
    if abs(error) < 3000:
        CutebotPro.pwm_cruise_control(0, 0)
        # check for magnet at exit
        if magnet_detect() > 250 and magnet_count == 2:
            magnet_count = 3
        basic.pause(100)
        straighten_to_line()
        line = 1
    return line

#turns for line following
def turn_r():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel + (abs(error)/3000)*maxturnspeed
    rwheel = rwheel - (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)
def turn_l():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel - (abs(error)/3000)*maxturnspeed
    rwheel = rwheel + (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)

## Line Following Function ##
def follow_line():
    global lwheel, rwheel, error
 
    # get the line offset
    error = CutebotPro.get_offset()
 
    # make the left side of line the center
    # error = error + 1000
 
    # if detects no line
    if abs(error) == 3000:
        lwheel = 0
        rwheel = 0
 
         #turn on both headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
     # if detects a big line
     #### Intersection ####
     # if detects a big line (error is less than 100)
    if abs(error) < 100:
        if error > 0: # robot is to the left of intersection (make a big right turn)
            error = 3000/error
            turn_r()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
        elif error < 0: # robot is to the right of intersection (make a big left turn)
            error = 3000/error
            turn_l()
            basic.pause(100)
             #yellow light
            CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)

     # too far left
    if error > 0:
        turn_r()
         # turn on left headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
     # too far right
    if error < 0:
        turn_l()
         #turn on right headlight (red)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
 
 
    # reset speed and headlights
    CutebotPro.turn_off_all_headlights()
    lwheel = 10
    rwheel = 10
 
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
    basic.pause(5)


# function for checking if wall is too close and backing up:
def check_if_too_close():
    sonar = abs(CutebotPro.ultrasonic(SonarUnit.CENTIMETERS))
    if sonar < 5: #check what is too close
        # move back a distance depending on how close
        dist = 5-sonar
        CutebotPro.distance_running(CutebotProOrientation.RETREAT, dist, CutebotProDistanceUnits.CM)

#functions for turning and moving forward
def check_distance():
    check_if_too_close()
    return CutebotPro.ultrasonic(SonarUnit.CENTIMETERS)

def turn_left():
    CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 90)
    #CutebotPro.trolley_speed_steering(50, CutebotProTurn.LEFT, 90)

    basic.pause(100)

def turn_right():
    CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 90)
    #CutebotPro.trolley_speed_steering(50, CutebotProTurn.RIGHT, 90)
    basic.pause(100)

def move_forward():
    CutebotPro.pwm_cruise_control(20, 20)
    line_found = 0
    while line_found == 0:
        line_found = detect_line()
    CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)
    basic.pause(100)

## TRANSMISSION FUNCTION ##
def on_button_pressed_a():
    basic.pause(1000)
    for i in range(len(path)):
        radio.send_value("step", path[i])
        basic.pause(700)  # Small delay for good transmission

## CELEBRATE FUNCTION ##
def total(bpm):
   CutebotPro.pwm_cruise_control(0,100)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff0000)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x7f00ff)
   music.play(music.string_playable("C", bpm),
                music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff8000)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x007fff)
   music.play(music.string_playable("C", bpm),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xffff00)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
   music.play(music.string_playable("C", bpm),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.pwm_cruise_control(100,0)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xffff00)
   music.play(music.string_playable("C", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ffff)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff8000)
   music.play(music.string_playable("C5", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x007fff)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff0000)
   music.play(music.string_playable("F", bpm),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x7f00ff)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff00ff)
   music.play(music.string_playable("F", bpm),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff00ff)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
   CutebotPro.pwm_cruise_control(0,100)
   music.play(music.string_playable("E", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff00ff)
   CutebotPro.pwm_cruise_control(100,0)
   music.play(music.string_playable("A", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff00ff)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
   CutebotPro.pwm_cruise_control(0,100)
   music.play(music.string_playable("E", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
   CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff00ff)
   CutebotPro.pwm_cruise_control(100,0)
   music.play(music.string_playable("A", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   
###### MAIN CODE ######
end = 0
#control.in_background(onIn_background)

## LINE FOLLOWING
#set variables
lwheel = 20
rwheel = 20
error = 0
maxturnspeed = 50

# set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)

#Run line follow till magnet detected then stop

while (magnet_detect() == 0):
   follow_line()
#stop robot
CutebotPro.pwm_cruise_control(0, 0)
basic.pause(100)
CutebotPro.turn_off_all_headlights()


## START MAZE ##
# be square with maze:
CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 90)
CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)


#grid_type: List[number] = [] #Java script, defines array as an integer array
#intersection: List[number] = []

#originate empty path taken
path: List[number] = []
first_move_done = False
maze_exit = False
magnet_count = 1

#maze navigation before exit magnet is located
while magnet_count < 3:
    mag = magnet_detect()
    #magnet found
    if mag >= 250:
        CutebotPro.single_headlights(CutebotProRGBLight.RGBL, 0, 255, 0)
        CutebotPro.single_headlights(CutebotProRGBLight.RGBR, 0, 255, 0)
        magnet_count+=1
       #magnet inside maze located
        if magnet_count == 2:
           path.append(4)
           basic.show_number(4)
    
    #end mazed navigation
    if magnet_count == 3:
        maze_exit = True
        led.plot(0, 0)

    #continue maze navigation
    else:
    # Look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        if left > 16:
            move_forward()
            path.append(2)
            basic.show_number(2)
        else:
        # Look forward
            turn_right()
            front = check_distance()
            basic.pause(100)
            if front > 16:
                move_forward()
                path.append(1)
                basic.show_number(1)
            else:
            # Look right
                turn_right()
                right = check_distance()
                basic.pause(100)
                if right > 16:
                    move_forward()
                    path.append(3)
                    basic.show_number(3)
                else:
                    # Dead end
                    turn_right()
                    move_forward()
                    path.append(0)
                    basic.show_number(0)

# play celebration!!
end = 1
music.stop_all_sounds()
total(130)

# send path to other robot:
input.on_button_pressed(Button.A, on_button_pressed_a)
radio.set_group(1)