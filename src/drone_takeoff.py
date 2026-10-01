#! /usr/bin/env python
import rospy
from std_msgs.msg import Empty

def drone_takeoff():
    pub = rospy.Publisher('/takeoff', Empty, queue_size=1)
    # rate = rospy.Rate(1)
    rospy.sleep(1)
    pub.publish(Empty())
    print(" taking off hopefully")

if __name__ == '__main__':
    rospy.init_node('drone_takeoff_node', anonymous=True)
    drone_takeoff()
    #rospy.spin()
