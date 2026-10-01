#!/usr/bin/env python

import rospy
import actionlib

from geometry_msgs import Pose, PoseStamped
from nav_msgs.msg import Odometry
from basics_exam.msg import RecordPoseResult, RecordPoseAction
class CheckDistActionServer(object):
    def __init__(self):
        self.server = actionlib.SimpleActionServer('/rec_pose_as', RecordPoseAction, self.execute, False)
        self.server.start()
        

    def execute(self, goal):
        rospy.loginfo("Recording positions...")
        positions = []  # List to store recorded positions

        self.start_time = None
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)

        def odom_callback(msg):
            pose = msg.pose.pose
            positions.append((pose.position.x, pose.position.y, pose.position.z))

        odom_sub = rospy.Subscriber('/your_drone/odom_topic', Odometry, odom_callback)

    # Record positions for 20 seconds
        rospy.sleep(20)

        odom_sub.unregister()

        result = RecordPoseResult()
        result.positions = positions

        self.server.set_succeeded(result)

if __name__ == '__main__':
    rospy.init_node('check_distance_action_server_node')
    server = CheckDistActionServer()
    rospy.spin()

    
