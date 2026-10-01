#! /usr/bin/env python
import rospy
import actionlib
from std_srvs.srv import Empty
from basics_exam.srv import CustomServiceMessage, CustomServiceMessageResponse
from basics_exam.msg import RecordPoseAction, RecordPoseActionGoal
from geometry_msgs.msg import Pose


#Start the distance motion service 
class Main_Program():
    rospy.wait_for_service('/motion_service')
    try:
        start_motion = rospy.ServiceProxy('/motion_service', Empty)
        response = start_motion()
        if response:
            print("Initial motion service started successfully.")
        else:
            print("Initial motion service failed to start.")
    except rospy.ServiceException as e:
        print("Service call failed:", e)
        # Start the distance motion service
    rospy.wait_for_service('/dist_motion_service')
    try:
        start_distance_motion = rospy.ServiceProxy('/dist_motion_service', CustomServiceMessage )
        response = start_distance_motion()
        if response.success:
            print(f"Distance motion service started successfully. Distance moved: {response.distance} meters.")
        else:
            print("Distance motion service failed to start.")
    except rospy.ServiceException as e:
        print("Service call failed:", e)

    # Start the recording action server
    client = actionlib.SimpleActionClient('/rec_pose_as', RecordPoseAction)
    client.wait_for_server()

    goal = RecordPoseActionGoal()
    client.send_goal(goal)

    client.wait_for_result()
    result = client.get_result()

       # Print the last recorded pose
    if result:
        last_pose = result.positions[-1]
        print(f"Last recorded pose: x={last_pose.x}, y={last_pose.y}, z={last_pose.z}")
    else:
        print("No positions recorded.")

if __name__ == '__main__':
    rospy.init_node('main_program')
    Main_Program()

