#!/usr/bin/env python

import rospy					#import the python library for ROS
from open_manipulator_msgs.msg import JointPosition	#import JointPosition message from the open_manipulator_msgs package
from open_manipulator_msgs.srv import SetJointPosition
from open_manipulator_msgs.msg import KinematicsPose
from open_manipulator_msgs.srv import SetKinematicsPose
from geometry_msgs.msg import Pose
import math

def callback(msg):				#define a function called 'callback' that receives a parameter named 'msg'
	print "positions:"
	print msg.pose.position.x
	print msg.pose.position.y
	print msg.pose.position.z

	print "orientations:"			
	print msg.pose.orientation.w
	print msg.pose.orientation.x
	print msg.pose.orientation.y
	print msg.pose.orientation.z

def talker():
	rospy.init_node('OM_publisher')	#Initiate a Node called 'OM_publisher'
	set_kinematics_position = rospy.ServiceProxy('/goal_joint_space_path_to_kinematics_position', SetKinematicsPose)
        set_gripper_position = rospy.ServiceProxy('/goal_tool_control', SetJointPosition)
	
	#while not rospy.is_shutdown():
	kinematics_pose = KinematicsPose()
	kinematics_pose.pose.position.x = 0.287
	kinematics_pose.pose.position.y = 0.0
	kinematics_pose.pose.position.z = 0.194
	resp1 = set_kinematics_position('planning_group', 'gripper', kinematics_pose, 3)

	sub_kinematics_pose = rospy.Subscriber('/gripper/kinematics_pose', KinematicsPose, callback)

	gripper_position = JointPosition()
	gripper_position.joint_name = ['gripper']
	gripper_position.position =  [0.01]	# -0.01 for fully close and 0.01 for fully open
	respg2 = set_gripper_position('planning_group',gripper_position, 3)

	rospy.sleep(3)
	kinematics_pose = KinematicsPose()
	kinematics_pose.pose.position.x = 0.0
	kinematics_pose.pose.position.y = 0.276
	kinematics_pose.pose.position.z = 0.192
	resp1 = set_kinematics_position('planning_group', 'gripper', kinematics_pose, 3)

	rospy.sleep(3)
	sub_kinematics_pose = rospy.Subscriber('/gripper/kinematics_pose', KinematicsPose, callback)
	

if __name__== '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
