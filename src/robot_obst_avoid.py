#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class robotmovenode(object):

    def __init__(self):

        self._laser_sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, self.callback)
        self._laser_scan = LaserScan()
        self._cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self._twist_move = Twist()
        rospy.spin()
        


    def callback(self, msg):
        self._laser_scan = msg
        print ('Value at 0 degrees:')
        print (self._laser_scan.ranges[0])
        print ('Value at 90 degrees:')
        print (self._laser_scan.ranges[360])
        print ('Value at 180 degrees:')
        print (self._laser_scan.ranges[719])
        self.laser_scan_to_twist()
        return self._laser_scan

       
    def laser_scan_to_twist(self):
   	if self._laser_scan.ranges[360]>1:
            self._twist_move.linear.x = 0.1
            self._twist_move.angular.z = 0
            
                
        if self._laser_scan.ranges[360]<1:
            self._twist_move.linear.x = 0
            self._twist_move.angular.z = 0.5

        if self._laser_scan.ranges[0]<1:
            self._twist_move.linear.x = 0
            self._twist_move.angular.z = 0.5

        if self._laser_scan.ranges[719]<1:
            self._twist_move.linear.x = 0
            self._twist_move.angular.z = -0.5

        else:
            pass  
      
        self._cmd_pub.publish(self._twist_move)
        
if __name__ == '__main__':
    rospy.init_node('obst_avoid_node')
    robotmovenode_object = robotmovenode()
    rate = rospy.Rate(2)

while not rospy.is_shutdown():                         
    # Create a loop that will go until someone stops the program execution
    robotmovenode_object.laser_scan_to_twist()
    rate.sleep()       
