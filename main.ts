let mag: number;
let left: number;
let front: number;
let right: number;
// #####FUNCTIONS######
// magnet checking function
function magnet_detect(): number {
    let mag = 0
    let magY = input.magneticForce(Dimension.Y)
    let magX = input.magneticForce(Dimension.X)
    let magZ = input.magneticForce(Dimension.Z)
    //  take the distance so you can sense in any direction
    let force = Math.pow(magX * magX + magY * magY + magZ * magZ, .5)
    if (force >= 500) {
        mag = 1
        //  turn headlights green
        CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
        CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
    }
    
    return mag
}

// # BACKGROUND MUSIC
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
    missionImpossibleMusic(350)
    
}

// # DIRECTION CORRECTION FUNCTIONS
function straighten_to_line() {
    let speed: number;
    // keep counter to break while loop
    let count = 0
    let error = CutebotPro.getOffset()
    //  turn on headlights(pink = 247, 25, 236)
    CutebotPro.singleHeadlights(CutebotProRGBLight.RGBL, 247, 25, 236)
    CutebotPro.singleHeadlights(CutebotProRGBLight.RGBR, 247, 25, 236)
    // keep turning till we are straight
    while (Math.abs(error) > 0 && count < 15) {
        //  update count of while loop iterations so we can prevent getting stuck
        count = count + 1
        // get offset
        error = CutebotPro.getOffset()
        //  set turn speed
        speed = 50 + Math.abs(error) / 3000 * 50
        //  turn right
        if (error > 0) {
            // turn on right headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(CutebotProRGBLight.RGBR, 51, 255, 252)
            CutebotPro.pwmCruiseControl(speed, 0)
            basic.pause(30)
        } else if (error < 0) {
            //  turn left
            // turn on left headlight(blue = 51, 255, 252)
            CutebotPro.singleHeadlights(CutebotProRGBLight.RGBL, 51, 255, 252)
            CutebotPro.pwmCruiseControl(speed * -1, 0)
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
        basic.pause(100)
        straighten_to_line()
        line = 1
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
    let sonar = CutebotPro.ultrasonic(SonarUnit.Centimeters)
    if (sonar < 5) {
        // check what is too close
        //  move back a distance depending on how close
        dist = 5 - sonar
        CutebotPro.distanceRunning(CutebotProOrientation.Retreat, dist, CutebotProDistanceUnits.Cm)
    }
    
}

// ##functions for turning and moving forward
function check_distance(): number {
    check_if_too_close()
    return CutebotPro.ultrasonic(SonarUnit.Centimeters)
}

function turn_left() {
    CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 90)
    basic.pause(100)
}

function turn_right() {
    CutebotPro.trolleySteering(CutebotProTurn.RightInPlace, 90)
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

// # TRANSMISSION
//  Small delay for good transmission
// # CELEBRATE
function total(bpm: number) {
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
    CutebotPro.pwmCruiseControl(0, 100)
    music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
    CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff00ff)
    CutebotPro.pwmCruiseControl(100, 0)
    music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0xff00ff)
    CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0x00ff00)
    CutebotPro.pwmCruiseControl(0, 100)
    music.play(music.stringPlayable("E", bpm * 2), music.PlaybackMode.UntilDone)
    CutebotPro.colorLight(CutebotProRGBLight.RGBL, 0x00ff00)
    CutebotPro.colorLight(CutebotProRGBLight.RGBR, 0xff00ff)
    CutebotPro.pwmCruiseControl(100, 0)
    music.play(music.stringPlayable("A", bpm * 2), music.PlaybackMode.UntilDone)
}

// ##### MAIN CODE ######
// control.in_background(onIn_background)
// # LINE FOLLOWING
// set variables
let lwheel = 20
let rwheel = 20
let error = 0
let maxturnspeed = 50
//  set starting speed
CutebotPro.pwmCruiseControl(lwheel, rwheel)
basic.pause(50)
// Run line follow till magnet detected then stop
while (magnet_detect() == 0) {
    follow_line()
}
// stop robot
CutebotPro.pwmCruiseControl(0, 0)
basic.pause(100)
CutebotPro.turnOffAllHeadlights()
// # START MAZE
//  be square with maze:
CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 90)
CutebotPro.distanceRunning(CutebotProOrientation.Advance, 15.35, CutebotProDistanceUnits.Cm)
// originate maze matrix and depth first search variables
// N = 5
// M = 6
// field = []
// for j in range(N):
// row = []
// for i in range(M):
// row.append(0)
// field.append(row)
let grid_type : number[] = []
// Java script, defines array as an integer array
let intersection : number[] = []
// originate empty path taken
let path : number[] = []
let first_move_done = false
let maze_exit = false
let magnet_count = 1
// maze navigation before exit magnet is located
while (magnet_count < 3) {
    mag = magnet_detect()
    // magnet found
    if (mag >= 200) {
        magnet_count += 1
        CutebotPro.trolleySteering(CutebotProTurn.LeftInPlace, 30)
        CutebotPro.trolleySteering(CutebotProTurn.RightInPlace, 30)
        // magnet inside maze located
        if (magnet_count == 2) {
            path.push(4)
        }
        
    }
    
    // end mazed navigation
    if (magnet_count == 3) {
        maze_exit = true
    } else {
        // continue maze navigation
        //  Look left
        turn_left()
        left = check_distance()
        basic.pause(100)
        if (left > 16) {
            move_forward()
            path.push(2)
        } else {
            //  Look forward
            turn_right()
            front = check_distance()
            basic.pause(100)
            if (front > 16) {
                move_forward()
                path.push(1)
            } else {
                //  Look right
                turn_right()
                right = check_distance()
                basic.pause(100)
                if (right > 16) {
                    move_forward()
                    path.push(3)
                } else {
                    //  Dead end
                    turn_right()
                    move_forward()
                    path.push(0)
                }
                
            }
            
        }
        
    }
    
}
//  play celebration!!
total(130)
//  send path to other robot:
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    basic.pause(1000)
    for (let i = 0; i < path.length; i++) {
        radio.sendValue("step", path[i])
        basic.pause(700)
    }
})
radio.setGroup(1)
