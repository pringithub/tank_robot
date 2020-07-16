#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy



class ROSTANK_JOY_TO_CMD_VEL:

    def __init__(self):

        self.joy_sub = rospy.Subscriber('/joy', Joy, self.cb, queue_size=1)
        self.cmdvel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    def cb(self, data):

        t = Twist()
        t.linear.x  = data.axes[1] # xbox left up
        t.angular.y = -data.axes[3] # xbox right up

        self.cmdvel_pub.publish(t)
     
 
if __name__=='__main__':
    rospy.init_node('rostank_joy2cmdvel')
    try:
        s = ROSTANK_JOY_TO_CMD_VEL()
        rospy.spin()
    except KeyboardInterrupt:
        rospy.logerr('Ctrl-C pressed .. exiting now')

	
