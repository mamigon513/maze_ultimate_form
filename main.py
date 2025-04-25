######FUNCTIONS######

## magnet checking function (return 1/0 for true/false)
def magnet_detect(thresh):
    # variable to determine if we detected a magnet (boolean)
    mag = 0
    # find the magnitude in each direction:
    magY = input.magnetic_force(Dimension.Y)
    magX = input.magnetic_force(Dimension.X)
    magZ = input.magnetic_force(Dimension.Z)
    # take the distance so you can sense in any direction
    force = Math.pow((magX*magX + magY*magY + magZ*magZ), .5)
    #magnet detected:
    if force >= thresh:
        mag = 1
        # turn headlights green
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
        # pause robot for 1 sec
        CutebotPro.pwm_cruise_control(0, 0)
        basic.pause(1000)
    return mag

## dead end function (depth-first search, complexity pts)
def dead_end(displacement):
    if displacement != 1:
        #go back to last intersection
        for i in range(displacement - 1): #move one square less than the displacement
            direct = path[len(path)-(i+2)] #read corresponding move that led to the dead end
            #move based on previous directions that led from last intersection to dead end
            if direct == 1:
                move_forward()
                basic.show_number(1)
            elif direct == 2:
                #left turn becomes a right turn
                move_forward()
                turn_right()
                basic.show_number(3)
            elif direct == 3:
                #right turn becomes a left turn
                move_forward()
                turn_left()
                basic.show_number(2)
    move_forward() #automatically leave dead end square if disp=1, add one forward move to sequence if disp>1


## BACKGROUND MUSIC FUNCTIONS ## (creativity pts)

## music function
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

## music play in background function
def onIn_background():
    global end
    music.set_volume(75)
    while end  ==  0:
        missionImpossibleMusic(350)
        basic.pause(500)
    pass


## DIRECTION CORRECTION FUNCTIONS ##

## robot straightening function
def straighten_to_line():
    #keep counter to break while loop
    count = 0
    error = CutebotPro.get_offset()
    # -1 is left 1 is right
    #which wheel to pivot
    wheel = error/abs(error)
    # turn on headlights(pink = 247, 25, 236)
    CutebotPro.single_headlights(CutebotProRGBLight.RGBL, 247, 25, 236)
    CutebotPro.single_headlights(CutebotProRGBLight.RGBR, 247, 25, 236)
    #keep turning till we are straight
    while(abs(error) > 0 and count < 4):
        # update count of while loop iterations so we can prevent getting stuck
        count = count + 1
        #get offset
    
        error = CutebotPro.get_offset()
        # set turn speed
        speed = 50 + (abs(error)/3000)*50
        
        if error > 0:
            #turn on right headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(CutebotProRGBLight.RGBR, 51, 255, 252)
            if wheel == 1: #pivot right wheel
                CutebotPro.pwm_cruise_control(speed, 0)
            elif wheel == -1: # pivot left wheel
                CutebotPro.pwm_cruise_control(0, speed*-1)
            basic.pause(30)
        
        elif error < 0:
            #turn on left headlight(blue = 51, 255, 252)
            CutebotPro.single_headlights(CutebotProRGBLight.RGBL, 51, 255, 252)
            if wheel == 1: #pivot right wheel
                CutebotPro.pwm_cruise_control(speed*-1, 0)
            elif wheel == -1: #pivot left wheel
                CutebotPro.pwm_cruise_control(0, speed)
            basic.pause(30)
        # turn off headlights
        CutebotPro.turn_off_all_headlights()
        CutebotPro.pwm_cruise_control(0, 0)
        basic.pause(50)
        error = CutebotPro.get_offset()

## black line detecing function
def detect_line():
    global magnet_count
    # get the line tracking offset
    error = CutebotPro.get_offset()
    line = 0
    # detects black line
    if abs(error) < 3000:
        CutebotPro.pwm_cruise_control(0, 0)
        # check for magnet at exit
        if magnet_detect(400) == 1 and magnet_count == 2:
            magnet_count = 3
            basic.pause(100)
        else:
            basic.pause(100)
            straighten_to_line()
            line = 1
    return line


## LINE FOLLOWING FUNCTIONS ##

## right turn function
def turn_r():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel + (abs(error)/3000)*maxturnspeed
    rwheel = rwheel - (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)

## left turn function
def turn_l():
    global lwheel, rwheel, maxturnspeed
    lwheel = lwheel - (abs(error)/3000)*maxturnspeed
    rwheel = rwheel + (abs(error)/3000)*maxturnspeed
     # Set the change
    CutebotPro.pwm_cruise_control(lwheel, rwheel)
     #delay 0.05 sec
     #delay 0.01 sec
    basic.pause(10)

## main line following function
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


## PROXIMITY CORRECTION FUNCTIONS ##

## checking if wall is too close and backing up functions
def check_if_too_close():
    sonar = abs(CutebotPro.ultrasonic(SonarUnit.CENTIMETERS))
    if sonar < 5: #check what is too close
        # move back a distance depending on how close
        dist = 5-sonar
        CutebotPro.distance_running(CutebotProOrientation.RETREAT, dist, CutebotProDistanceUnits.CM)

def check_distance():
    check_if_too_close()
    return CutebotPro.ultrasonic(SonarUnit.CENTIMETERS)


## MAZE MOVEMENT FUNCTIONS ##

## 90 degree left turn function
def turn_left():
    CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 90)
    #CutebotPro.trolley_speed_steering(50, CutebotProTurn.LEFT, 90)
    basic.pause(100)

## 90 degree right turn function
def turn_right():
    CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 90)
    #CutebotPro.trolley_speed_steering(50, CutebotProTurn.RIGHT, 90)
    basic.pause(100)

## move forward function
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
    int_count = 0
    for i in range(len(path)):
        radio.send_value("step", path[i])
        if path[i] == 0:
            val = disp_array[int_count]
            radio.send_value("int",val)
            int_count+=1
        basic.pause(700)  # Small delay for good transmission


## CELEBRATE FUNCTION ##
def total(bpm):
    #orient out of maze
    CutebotPro.pwm_cruise_control(100,100)
    pause(1000)

    for i in range(2):
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
        CutebotPro.pwm_cruise_control(0,50)
        music.play(music.string_playable("E", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff00ff)
        CutebotPro.pwm_cruise_control(50,0)
        music.play(music.string_playable("A", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0xff00ff)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x00ff00)
        CutebotPro.pwm_cruise_control(0,50)
        music.play(music.string_playable("E", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
        CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.color_light(CutebotProRGBLight.RGBR, 0xff00ff)
        CutebotPro.pwm_cruise_control(50,0)
        music.play(music.string_playable("A", bpm*2),
                    music.PlaybackMode.UNTIL_DONE)
   


###### MAIN CODE ######
end = 0
control.in_background(onIn_background) #runs mission impossible music


## LINE FOLLOWING ##
#set variables
lwheel = 20
rwheel = 20
error = 0
maxturnspeed = 70
disp = 25
disp_array: List[number] = [] #Java script, defines array as an integer array (this notation is used for all arrays)

#set starting speed
CutebotPro.pwm_cruise_control(lwheel, rwheel)
basic.pause(50)

#run line follow till magnet detected
while (magnet_detect(500) == 0):
   follow_line()

#stop robot
CutebotPro.pwm_cruise_control(0, 0)
basic.pause(100)
CutebotPro.turn_off_all_headlights()


## START MAZE ##
#be square with maze:
#CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 90)
#CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 5, CutebotProDistanceUnits.CM)
CutebotPro.trolley_steering(CutebotProTurn.LEFT_IN_PLACE, 90)
#move_forward()
CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 15.35, CutebotProDistanceUnits.CM)


#originate arrays for dead end navigation and depth-first search code
grid_type: List[number] = [] #Java script, defines array as an integer array
intersection: List[number] = []

#originate empty path taken by robot
path: List[number] = []

#set magnet count to one after the maze is entered
magnet_count = 1

## MAZE NAVIGATION BEFORE MAGNET IS FOUND ##
while magnet_count < 2: #loop until a second magnet is found
    mag = magnet_detect(500)

    if mag == 1: #magnet found
        magnet_count+=1
          
    if magnet_count == 2: #magnet inside maze located
        path.append(5)
        basic.show_number(5)
        turn_right()
        turn_right()
        move_forward()
        path.append(1)
        basic.show_number(1)

    #continue maze navigation
    else:
        #check forward 
        front = check_distance()
        basic.pause(100)

        #look right
        turn_right()
        right = check_distance()
        basic.pause(100)
        
        #look left
        turn_left()
        turn_left()
        left = check_distance()
        basic.pause(100)

        # Maze nav -- Depth first
        if left>disp and front>disp and right>disp: #evaluate where walls are encountered
            grid = 1
            grid_type.append(grid) #store which type of grid/wall layout is encountered, 8 types total
            intersection.append(len(grid_type)) #note where intersections occur
        elif left > disp and front > disp:
            grid = 2
            grid_type.append(grid)
            intersection.append(len(grid_type)) #considered intersection
        elif left > disp and right > disp:
            grid = 3
            grid_type.append(grid)
            intersection.append(len(grid_type)) #considered intersection
        elif front > disp and right > disp:
            grid = 4
            grid_type.append(grid)
            intersection.append(len(grid_type)) #considered intersection
        elif left > disp:
            grid = 5
            grid_type.append(grid)
        elif front > disp:
            grid = 6
            grid_type.append(grid)
        elif right > disp:
            grid = 7
            grid_type.append(grid)
        else:
            grid = 8
            grid_type.append(grid)

        # Movement Decision (left favoring)
        if left > disp: #go left
            move_forward()
            path.append(2)
            basic.show_number(2)

        elif front > disp: #go forward
            turn_right()
            move_forward()
            path.append(1)
            basic.show_number(1)

        elif right > disp: #go right
            turn_right()
            turn_right()
            move_forward()
            path.append(3)
            basic.show_number(3)

        else:
            #dead end encountered
            turn_left()
            path.append(0)
            basic.show_number(0)
            #run dead end navigation code
            displacement = (len(path) - intersection[len(intersection)-1]) #calculate displacement between last intersection and dead end
            disp_array.append(displacement) #store displacements between intersections and dead ends
            basic.show_number(displacement)
            dead_end(displacement)


## MAZE NAVIGATION TO EXIT MAZE ##
while magnet_count < 3:
    
    #search for magnet
    mag = magnet_detect(150)

    #exit magnet located
    if mag == 1:
        magnet_count+=1
        
    #end maze navigation if magnet is found
    if magnet_count == 3:
        led.plot(0, 0)

    else:
        #check forward
        front = check_distance()
        basic.pause(100)

        #look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        
        #look right
        turn_right()
        turn_right()
        right = check_distance()
        basic.pause(100)

        # Maze nav -- Depth first
        #same grid/wall pattern evaluation and storage as the previous loop
        if left>disp and front>disp and right>disp:
            grid = 1
            grid_type.append(grid)
            intersection.append(len(grid_type)) 
        elif left > disp and front > disp:
            grid = 2
            grid_type.append(grid)
            intersection.append(len(grid_type))
        elif left > disp and right > disp:
            grid = 3
            grid_type.append(grid)
            intersection.append(len(grid_type))
        elif front > disp and right > disp:
            grid = 4
            grid_type.append(grid)
            intersection.append(len(grid_type))
        elif left > disp:
            grid = 5
            grid_type.append(grid)
        elif front > disp:
            grid = 6
            grid_type.append(grid)
        elif right > disp:
            grid = 7
            grid_type.append(grid)
        else:
            grid = 8
            grid_type.append(grid)

        # Movement Decision (right favoring)
        if right > disp: #go right
            move_forward()
            path.append(3)
            basic.show_number(3)

        elif front > disp: #go forward
            turn_left()
            move_forward()
            path.append(1)
            basic.show_number(1)

        elif left > disp: #go left
            turn_left()
            turn_left()
            move_forward()
            path.append(2)
            basic.show_number(2)

        else:
            #dead end encountered
            #same as before, excpet robot is now facing right and turns right to exit dead end
            turn_right()
            path.append(0)
            basic.show_number(0)
            displacement = (len(path) - intersection[len(intersection)-1]-2) #subtract two from length of path to account for magnet detection adding to path length
            disp_array.append(displacement)
            basic.show_number(displacement)
            dead_end(displacement)



## PLAY CELEBRATION!! ##
end = 1
music.stop_all_sounds()
total(130)
music.stop_all_sounds()
CutebotPro.color_light(CutebotProRGBLight.RGBL, 0x000000)
CutebotPro.color_light(CutebotProRGBLight.RGBR, 0x000000)
CutebotPro.pwm_cruise_control(0, 0)


## TRANSMIT PATH TO SECOND MICROBIT ##
input.on_button_pressed(Button.A, on_button_pressed_a)
radio.set_group(10) #radio channel 10