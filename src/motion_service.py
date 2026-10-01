#! /usr/bin/env python
import rospy

from basics_exam.msg import CustomActionMsgFeedback, CustomActionMsgResult, CustomActionMsgAction
from std_srvs.srv import Empty, EmptyResponse
from square_motion import SquareMotion

def my_callback(request):
    print("My_callback has been called")
    SquareMotion() 
    return EmptyResponse() # the service Response class, in this case EmptyResponse
    #return MyServiceResponse(len(request.words.split())) 

rospy.init_node('motion_service') # name is the realitve launch 
print("am i here yet? - yes")
my_service = rospy.Service('/motion_service', Empty, my_callback) # create the Service called my_service with the defined callback
rospy.spin() # maintain the service open.
# service = rospy.Service( "/move_bb8_in_square_custom", BB8CustomServiceMessage, handle_bb8_square_movement)
