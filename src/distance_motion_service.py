#!/usr/bin/env python
import rospy
from basics_exam.msg import RecordPoseAction, RecordPoseActionFeedback, RecordPoseActionResult
from std_srvs.srv import Empty, EmptyResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from basics_exam.srv import CustomServiceMessage, CustomServiceMessageRequest
import time
class DistanceMotionService:

    def __init__(self):
        print("we are in init")
        rospy.init_node('distance_motion_service')
        
        self.motion_service = rospy.Service('/dist_motion_service', Empty, self.motion_request_control)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
            
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
    
        self.start_position_x = None
        self.end_position_x = None
        self.distance_move = 0
    
    def odom_callback(self, msg):
        if self.start_time is not None:
            curr_time = rospy.Time.now()
            time_dif = curr_time - self.start_time
            if time_dif.to_sec() <= 60.0:
                linear_x = msg.twist.twist.linear.x
                self.distance_moved += linear_x * time_dif.to_sec()
            else:
                rospy.logwarn("Took longer than 60 seconds. Service has failed :(")

        def calculate_distance(self):
            if self.start_position_x is not None and self.end_position_x is not None:
             self.distance_moved = abs(self.end_position_x - self.start_position_x)

        def stop_condition_met(self):
         return self.distance_moved >= 8.0

        def motion_request_control(self,response):
            print("were in motion control")
            self.distance_moved = 0.0
            self.start_time = rospy.Time.now()
            Twist().linear.x = 0.5
            Twist().angular.z = 0.0
            rate = rospy.Rate(5) # 6 Hz sampling 
        # Set the start time to None initially
            
            self.start_time = None
            while not rospy.is_shutdown():
        # Publish the Twist message
                self.cmd_vel_pub.publish(Twist())
                print("in da loop")
                print(self.distance_moved)

        # Check if the distance moved is greater than or equal to 8.0
                if self.distance_moved >= 8.0:
            # If so, break out of the loop
                    break

if __name__ == '__main__':
    DistanceMotionService()
    print("main here")
    rospy.spin()
        
