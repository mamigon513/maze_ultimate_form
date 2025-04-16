let mag: number;
let front: number;
let right: number;
let left: number;
let grid: number;
let displacement: number;
// #####FUNCTIONS######
// magnet checking function (return 1/0 for true/false)
function magnet_detect(thresh: number): number {
    let mag = 0
    let magY = input.magneticForce(Dimension.Y)
    let magX = input.magneticForce(Dimension.X)
    let magZ = input.magneticForce(Dimension.Z)
    //  take the distance so you can sense in any direction
    let force = Math.pow(magX * magX + magY * magY + magZ * magZ, .5)
    if (force >= thresh) {
        mag = 1
        //  turn headlights green
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
        //  pause robot for 1 sec
        CutebotPro.pwmCruiseControl(0, 0)
        basic.pause(1000)
    }
    
    return mag
}

// # dead end function (depth-first search)
function dead_end(displacement: number) {
    let direct: number;
    if (displacement != 1) {
        // go back to last intersection
        for (let i = 0; i < displacement - 1; i++) {
            //  move one square less than the displacement
            direct = path[path.length - (i + 2)]
            if (direct == 1) {
                move_forward()
                basic.showNumber(1)
            } else if (direct == 2) {
                move_forward()
                turn_right()
                basic.showNumber(3)
            } else if (direct == 3) {
                move_forward()
                turn_left()
                basic.showNumber(2)
            }
            
        }
    }
    
    move_forward()
}

// # BACKGROUND MUSIC FUNCTION ##
function missionImpossibleMusic(bpm: number) {
    music.play(music.stringPlayable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("C5 C5 G4 G4 - G4 G4 G4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Fb4 Fb4 F4 F4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("G4 G4 - G4 G4 G4 Bb4 Bb4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("C5 C5 G4 G4 - G4 G4 G4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Fb4 Fb4 F4 F4", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 D5 D5 D5 D5 D5 D5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 Db5 Db5 Db5 Db5 Db5 Db5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("A6 G6 C5 C5 C5 C5 C5 C5 - -", bpm), music.PlaybackMode.UntilDone)
    music.play(music.stringPlayable("Bb4 C5 - -", bpm), music.PlaybackMode.UntilDone)
}

//  make music play in background
function onIn_background() {
    
    music.setVolume(100)
    while (end == 0) {
        missionImpossibleMusic(350)
        basic.pause(500)
    }
    
}

// # DIRECTION CORRECTION FUNCTIONS ##
function straighten_to_line() {
    let speed: number;
    // keep counter to break while loop
    let count = 0
    let error = CutebotPro.getOffset()
    //  -1 is left 1 is right
    // which wheel to pivot
    let wheel = error / Math.abs(error)
    //  turn on headlights(pink = 247, 25, 236)
    CutebotPro.singleHeadlights(CutebotProRGBLight.RGBL, 247, 25, 236)
    CutebotPro.singleHeadlights(CutebotProRGBLight.RGBR, 247, 25, 236)
    // keep turning till we are straight
    while (Math.abs(error) > 0 && count < 2) {
        //  update count of while loop iterations so we can prevent getting stuck
        count = count + 1
        // get offset
        error = CutebotPro.getOffset()
        //  set turn speed
        speed = 50 + Math.abs(error) / 3000 * 50
        if (error > 0) {
            // turn on right headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(CutebotProRGBLight.RGBR, 51, 255, 252)
            if (wheel == 1) {
                // pivot right wheel
                CutebotPro.pwmCruiseControl(speed, 0)
            } else if (wheel == -1) {
                //  pivot left wheel
                CutebotPro.pwmCruiseControl(0, speed * -1)
            }
            
            basic.pause(30)
        } else if (error < 0) {
            // turn on left headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(CutebotProRGBLight.RGBL, 51, 255, 252)
            if (wheel == 1) {
                // pivot right wheel
                CutebotPro.pwmCruiseControl(speed * -1, 0)
            } else if (wheel == -1) {
                // pivot left wheel
                CutebotPro.pwmCruiseControl(0, speed)
            }
            
            basic.pause(30)
        }
        
        //  turn off headlights
        CutebotPro.turnOffAllHeadlights()
        CutebotPro.pwmCruiseControl(0, 0)
        basic.pause(50)
        error = CutebotPro.getOffset()
    }
}

function detect_line(): number {
    
    //  get the line tracking offset
    let error = CutebotPro.getOffset()
    let line = 0
    //  detects black line
    if (Math.abs(error) < 3000) {
        CutebotPro.pwmCruiseControl(0, 0)
        //  check for magnet at exit
        if (magnet_detect(400) == 1 && magnet_count == 2) {
            magnet_count = 3
            basic.pause(100)
        } else {
            basic.pause(100)
            straighten_to_line()
            line = 1
        }
        
    }
    
    return line
}

// turns for line following
function turn_r() {
    
    lwheel = lwheel + Math.abs(error) / 3000 * maxturnspeed
    rwheel = rwheel - Math.abs(error) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec
    // delay 0.01 sec
    basic.pause(10)
}

function turn_l() {
    
    lwheel = lwheel - Math.abs(error) / 3000 * maxturnspeed
    rwheel = rwheel + Math.abs(error) / 3000 * maxturnspeed
    //  Set the change
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    // delay 0.05 sec
    // delay 0.01 sec
    basic.pause(10)
}

// # Line Following Function ##
function follow_line() {
    
    //  get the line offset
    error = CutebotPro.getOffset()
    //  make the left side of line the center
    //  error = error + 1000
    //  if detects no line
    if (Math.abs(error) == 3000) {
        lwheel = 0
        rwheel = 0
        // turn on both headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  if detects a big line
    // ### Intersection ####
    //  if detects a big line (error is less than 100)
    if (Math.abs(error) < 100) {
        if (error > 0) {
            //  robot is to the left of intersection (make a big right turn)
            error = 3000 / error
            turn_r()
            basic.pause(100)
            // yellow light
            CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xffff00)
        } else if (error < 0) {
            //  robot is to the right of intersection (make a big left turn)
            error = 3000 / error
            turn_l()
            basic.pause(100)
            // yellow light
            CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xffff00)
        }
        
    }
    
    //  too far left
    if (error > 0) {
        turn_r()
        //  turn on left headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
    }
    
    //  too far right
    if (error < 0) {
        turn_l()
        // turn on right headlight (red)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
    }
    
    //  reset speed and headlights
    CutebotPro.turnOffAllHeadlights()
    lwheel = 10
    rwheel = 10
    CutebotPro.pwmCruiseControl(lwheel, rwheel)
    basic.pause(5)
}

//  function for checking if wall is too close and backing up:
function check_if_too_close() {
    let dist: number;
    let sonar = Math.abs(CutebotPro.ultrasonic(SonarUnit.Centimeters))
    if (sonar < 5) {
        // check what is too close
        //  move back a distance depending on how close
        dist = 5 - sonar
        CutebotPro.distanceRunning(CutebotProOrientation.Retreat, dist, CutebotProDistanceUnits.Cm)
    }
    
}

// functions for turning and moving forward
function check_distance(): number {
    check_if_too_close()
    return CutebotPro.ultrasonic(SonarUnit.Centimeters)
}

function turn_left() {
    CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 90)
    // CutebotPro.trolley_speed_steering(50, CutebotProTurn.LEFT, 90)
    basic.pause(100)
}

function turn_right() {
    CutebotPro.trolleySteering(CutebotProTurn.RightInPlace, 90)
    // CutebotPro.trolley_speed_steering(50, CutebotProTurn.RIGHT, 90)
    basic.pause(100)
}

function move_forward() {
    CutebotPro.pwmCruiseControl(20, 20)
    let line_found = 0
    while (line_found == 0) {
        line_found = detect_line()
    }
    CutebotPro.distanceRunning(CutebotProOrientation.Advance, 15.35, CutebotProDistanceUnits.Cm)
    basic.pause(100)
}

// # TRANSMISSION FUNCTION ##
//  Small delay for good transmission
// # CELEBRATE FUNCTION ##
function total(bpm: number) {
    // orient out of maze
    CutebotPro.pwmCruiseControl(100, 100)
    pause(1000)
    for (let i = 0; i < 2; i++) {
        CutebotPro.pwmCruiseControl(0, 100)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff0000)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x7f00ff)
        music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff8000)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x007fff)
        music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xffff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
        music.play(music.stringPlayable("C", bpm), music.PlaybackMode.UntilDone)
        CutebotPro.pwmCruiseControl(100, 0)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xffff00)
        music.play(music.stringPlayable("C", bpm * 2), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ffff)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff8000)
        music.play(music.stringPlayable("C5", bpm * 2), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x007fff)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff0000)
        music.play(music.stringPlayable("F", bpm), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x7f00ff)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff00ff)
        music.play(music.stringPlayable("F", bpm), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff00ff)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
        CutebotPro.pwmCruiseControl(0, 50)
        music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff00ff)
        CutebotPro.pwmCruiseControl(50, 0)
        music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff00ff)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
        CutebotPro.pwmCruiseControl(0, 50)
        music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff00ff)
        CutebotPro.pwmCruiseControl(50, 0)
        music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
    }
}

// ##### MAIN CODE ######
let end = 0
// control.in_background(onIn_background)
// # LINE FOLLOWING
// set variables
let lwheel = 20
let rwheel = 20
let error = 0
let maxturnspeed = 70
let disp = 25
let disp_array : number[] = []
// Java script, defines array as an integer array
//  set starting speed
CutebotPro.pwmCruiseControl(lwheel, rwheel)
basic.pause(50)
// Run line follow till magnet detected then stop
while (magnet_detect(500) == 0) {
    follow_line()
}
// stop robot
CutebotPro.pwmCruiseControl(0, 0)
basic.pause(100)
CutebotPro.turnOffAllHeadlights()
// # START MAZE ##
//  be square with maze:
// CutebotPro.trolley_steering(CutebotProTurn.RIGHT_IN_PLACE, 90)
// CutebotPro.distance_running(CutebotProOrientation.ADVANCE, 5, CutebotProDistanceUnits.CM)
CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 90)
// move_forward()
CutebotPro.distanceRunning(CutebotProOrientation.Advance, 15.35, CutebotProDistanceUnits.Cm)
let grid_type : number[] = []
// Java script, defines array as an integer array
let intersection : number[] = []
// originate empty path taken
let path : number[] = []
let magnet_count = 1
// maze navigation before magnet is located
while (magnet_count < 2) {
    mag = magnet_detect(500)
    // magnet found
    if (mag == 1) {
        magnet_count += 1
    }
    
    // magnet inside maze located  
    if (magnet_count == 2) {
        path.push(5)
        basic.showNumber(5)
        turn_right()
        turn_right()
        move_forward()
        path.push(1)
        basic.showNumber(1)
    } else {
        // continue maze navigation
        // Check forward 
        front = check_distance()
        basic.pause(100)
        //  Look right
        turn_right()
        right = check_distance()
        basic.pause(100)
        //  Look left
        turn_left()
        turn_left()
        left = check_distance()
        basic.pause(100)
        //  Maze Nav -- Depth first (left favoring)
        if (left > disp && front > disp && right > disp) {
            grid = 1
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp && front > disp) {
            // note where intersections occur
            grid = 2
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp && right > disp) {
            grid = 3
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (front > disp && right > disp) {
            grid = 4
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp) {
            grid = 5
            grid_type.push(grid)
        } else if (front > disp) {
            grid = 6
            grid_type.push(grid)
        } else if (right > disp) {
            grid = 7
            grid_type.push(grid)
        } else {
            grid = 8
            grid_type.push(grid)
        }
        
        //  Movement Decision
        if (left > disp) {
            move_forward()
            path.push(2)
            basic.showNumber(2)
        } else if (front > disp) {
            turn_right()
            move_forward()
            path.push(1)
            basic.showNumber(1)
        } else if (right > disp) {
            turn_right()
            turn_right()
            move_forward()
            path.push(3)
            basic.showNumber(3)
        } else {
            //  Dead end
            turn_left()
            path.push(0)
            basic.showNumber(0)
            displacement = path.length - intersection[intersection.length - 1]
            disp_array.push(displacement)
            basic.showNumber(displacement)
            dead_end(displacement)
        }
        
    }
    
}
// # EXITING MAZE ##
while (magnet_count < 3) {
    mag = magnet_detect(400)
    // magnet found
    if (mag == 1) {
        magnet_count += 1
    }
    
    // magnet inside maze located
    // end maze navigation
    if (magnet_count == 3) {
        led.plot(0, 0)
    } else {
        // Check forward
        front = check_distance()
        basic.pause(100)
        //  Look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        //  Look right
        turn_right()
        turn_right()
        right = check_distance()
        basic.pause(100)
        //  Maze Nav -- Depth first (left favoring)
        if (left > disp && front > disp && right > disp) {
            grid = 1
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp && front > disp) {
            // note where intersections occur
            grid = 2
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp && right > disp) {
            grid = 3
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (front > disp && right > disp) {
            grid = 4
            grid_type.push(grid)
            intersection.push(grid_type.length)
        } else if (left > disp) {
            grid = 5
            grid_type.push(grid)
        } else if (front > disp) {
            grid = 6
            grid_type.push(grid)
        } else if (right > disp) {
            grid = 7
            grid_type.push(grid)
        } else {
            grid = 8
            grid_type.push(grid)
        }
        
        //  Movement Decision
        if (right > disp) {
            move_forward()
            path.push(3)
            basic.showNumber(3)
        } else if (front > disp) {
            turn_left()
            move_forward()
            path.push(1)
            basic.showNumber(1)
        } else if (left > disp) {
            turn_left()
            turn_left()
            move_forward()
            path.push(2)
            basic.showNumber(2)
        } else {
            //  Dead end
            turn_right()
            path.push(0)
            basic.showNumber(0)
            displacement = path.length - intersection[intersection.length - 1] - 2
            disp_array.push(displacement)
            basic.showNumber(displacement)
            dead_end(displacement)
        }
        
    }
    
}
//  play celebration!!
end = 1
music.stopAllSounds()
total(130)
music.stopAllSounds()
CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x000000)
CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x000000)
CutebotPro.pwmCruiseControl(0, 0)
//  send path to other robot:
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    let val: number;
    basic.pause(1000)
    let int_count = 0
    for (let i = 0; i < path.length; i++) {
        radio.sendValue("step", path[i])
        if (path[i] == 0) {
            val = disp_array[int_count]
            radio.sendValue("int", val)
            int_count += 1
        }
        
        basic.pause(700)
    }
})
radio.setGroup(1)
