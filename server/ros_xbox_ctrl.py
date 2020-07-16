# USAGE
# sudo python3 xbox_ctrl.py --no-video 1

import argparse
import move
import servo
import ultra
from xbox import xbox
import time
import threading

direction_command='no'
turn_command='no'

LOW_SPEED_MIN=0.5
HIGH_SPEED_MIN=0.9
LOW_SPEED_SET=50
HIGH_SPEED_SET=100
RAD=0.6



try:
    joy = xbox.Joystick()         #Initialize joystick
    NO_VIDEO=True
    if NO_VIDEO:
        import FPV_pub
        from FPV_pub import FPV
        fpv = FPV()
except Exception as e:
    print(e)
    print("Exiting")
    servo.clean_all()
    exit(1)

arm = servo.Arm()


def FPV_thread():
    fpv.capture_thread()


def move_wheels():

    (lx,ly)    = joy.leftStick()    #Returns tuple containing left X and Y axes (values -1.0 to 1.0)
    (rx,ry)    = joy.rightStick()   #Returns tuple containing right X and Y axes (values -1.0 to 1.0)

    if   ly>HIGH_SPEED_MIN:
        direction_cmd = 'forward'
        speed_set = HIGH_SPEED_SET
    elif ly>LOW_SPEED_MIN:
        direction_cmd = 'forward'
        speed_set = LOW_SPEED_SET
    elif ly<-LOW_SPEED_MIN:
        direction_cmd = 'backward'
        speed_set = LOW_SPEED_SET
    elif ly<-HIGH_SPEED_MIN:
        direction_cmd = 'backward'
        speed_set = HIGH_SPEED_SET
    else:
        direction_cmd = 'no'
        speed_set = HIGH_SPEED_SET # doesn't mattr

    if   rx>HIGH_SPEED_MIN:
        turn_cmd = 'right'
        speed_set = HIGH_SPEED_SET
    elif rx>LOW_SPEED_MIN:
        turn_cmd = 'right'
        speed_set = LOW_SPEED_SET
    elif rx<-LOW_SPEED_MIN:
        turn_cmd = 'left'
        speed_set = LOW_SPEED_SET
    elif rx<-HIGH_SPEED_MIN:
        turn_cmd = 'left'
        speed_set = HIGH_SPEED_SET
    else:
        turn_cmd = 'no'
        speed_set = HIGH_SPEED_SET # doesn't mattr
    
    move.move( speed_set, direction_cmd, turn_cmd, RAD)

def move_servos():

    lt = joy.leftTrigger()
    rt = joy.rightTrigger()
    lb = joy.leftBumper()
    rb = joy.rightBumper()

    if lt:
        arm.loosen()
    if rt:
        arm.clamp()
    if lb:
        arm.reach_out()
    if rb:
        arm.tuck_in()

    reset_arm = joy.Y()
    if reset_arm: # TODO should probably have this be a one time thing
        arm.start_position()

    camup = joy.dpadUp()
    camdown = joy.dpadDown()
    if camup:
        servo.camera_ang('lookup')
    if camdown:
        servo.camera_ang('lookdown')

def debug_servos():

    test0 = joy.dpadLeft()
    test1 = joy.dpadRight()
    test2 = joy.dpadUp()
    test3 = joy.dpadDown()
    if test0:
        arm.move_L12('pos')
    if test1:
        arm.move_L12('neg')
    if test2:
        arm.move_L13('pos')
    if test3:
        arm.move_L13('neg')        

    test4 = joy.A()
    test5 = joy.B()
    test6 = joy.X()
    test7 = joy.Y()
    if test4:
        arm.move_L14('pos')
    if test5:
        arm.move_L14('neg')
    if test6:
        arm.move_L15('pos')
    if test7:
        arm.move_L15('neg')

    print('{} {} {} {} {} {} {} {}'.format(test0,test1,test2,test3,test4,test5,test6,test7))
    arm.print_servo_pos()

def enable_stream(fpv):
    start = joy.Start()
    if start:
        fpv.set_stream(1)
        print('Stream Set')
    #
    stop = joy.Back()
    if stop:
        fpv.FindColor(0)
        fpv.WatchDog(0)
        fpv.set_stream(0) 
        print('Stream Unset')
    #
    find_color = joy.A()
    stop_find_color = joy.B()
    if find_color:
        fpv.FindColor(1)
    if stop_find_color:
        fpv.FindColor(0)

    watchdog = joy.X()
    stop_watchdog = joy.Y()
    if watchdog:
        fpv.WatchDog(1)
    if stop_watchdog:
        fpv.WatchDog(0)

    #print('{} {} {} {}'.format(start,stop,find_color,watchdog))

if __name__ == '__main__':
    # TODO look over this block ... 
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-v", "--no_video", type=bool, required=False,
    #                default=False, help="boolean for video or not")
    #args = vars(ap.parse_args())
    #NO_VIDEO =args["no_video"] #True if args["no_video"] else False
    #print(NO_VIDEO)
    NO_VIDEO=True

    print('Node starting ..')
    move.setup()
    
    if not NO_VIDEO:
        fps_threading=threading.Thread(target=FPV_thread)    #Define a thread for FPV and OpenCV
        fps_threading.setDaemon(True)                        #'True' means it is a front thread,it would close when the mainloop() closes
        fps_threading.start()                                #Thread starts
        print('Video Enabled')
    else:
        print("Video Disabled")

    time.sleep(2)
    print('Ready')

    while True:
        try:
            move_wheels()
            move_servos()
            if not NO_VIDEO:
                enable_stream(fpv)
            #debug_servos()

            #ultradist = round(ultra.checkdist(),2)
            #print('ly:{}  rx:{}  lt:{} rt:{} lb:{} rb:{}  ultra:{}'.format(round(ly,2),round(rx,2),lt,rt,lb,rb,ultradist)) 
            time.sleep(0.05)

        except KeyboardInterrupt:
            print('\nCtrl-C pressed. Exiting')
            joy.close()
            servo.clean_all()
            move.destroy()
            if not NO_VIDEO:
                FPV_pub.destroy()
            exit(0)
        except:
            print('[ERROR] Something went wrong')
            joy.close()
            servo.clean_all()
            move.destroy()
            if not NO_VIDEO:
                FPV_pub.destroy()
            exit(1)
