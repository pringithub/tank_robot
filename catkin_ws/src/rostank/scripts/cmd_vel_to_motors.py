#!/usr/bin/env python

import move 

import rospy
from geometry_msgs.msg import Twist

direction_command = 'no'
turn_command      = 'no'
LOW_SPEED_MIN  = 0.5
HIGH_SPEED_MIN = 0.9
LOW_SPEED_SET  = 50
HIGH_SPEED_SET = 100
RAD            = 0.6


class ROSTANK_CMD_VEL_TO_MOTORS:

    def __init__(self):
	move.setup() # initialize motors

        self.cmdvel_sub = rospy.Subscriber('/cmd_vel', Twist, self.cb, queue_size=1)

    def cb(self, data):
        f = data.linear.x
	r = data.angular.y

        if   f>HIGH_SPEED_MIN:
            direction_cmd = 'forward'
            speed_set = HIGH_SPEED_SET
        elif f>LOW_SPEED_MIN:
            direction_cmd = 'forward'
            speed_set = LOW_SPEED_SET
        elif f<-LOW_SPEED_MIN:
            direction_cmd = 'backward'
            speed_set = LOW_SPEED_SET
        elif f<-HIGH_SPEED_MIN:
            direction_cmd = 'backward'
            speed_set = HIGH_SPEED_SET
        else:
            direction_cmd = 'no'
            speed_set = HIGH_SPEED_SET # doesn't matter

        if   r>HIGH_SPEED_MIN:
            turn_cmd = 'right'
            speed_set = HIGH_SPEED_SET
        elif r>LOW_SPEED_MIN:
            turn_cmd = 'right'
            speed_set = LOW_SPEED_SET
        elif r<-LOW_SPEED_MIN:
            turn_cmd = 'left'
            speed_set = LOW_SPEED_SET
        elif r<-HIGH_SPEED_MIN:
            turn_cmd = 'left'
            speed_set = HIGH_SPEED_SET
        else:
            turn_cmd = 'no'
            speed_set = HIGH_SPEED_SET # doesn't matter

        move.move( speed_set, direction_cmd, turn_cmd, RAD )
       
if __name__=='__main__':
    rospy.init_node('rostank_cmdvel2motors')
    try:
        s = ROSTANK_CMD_VEL_TO_MOTORS()
        rospy.spin()
    except KeyboardInterrupt:
        move.destroy()


	
