#! /usr/bin/env python2.7

import rospy
import numpy as np
import sys
import time
import cv2
#from PIL import Image, ImageDraw, ImageFont
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import Image
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TestNode(object): 

	def __init__(self, queue_size=100):
		rospy.init_node('test')
		#self.sub = rospy.Subscriber("/cozmo/battery",BatteryState, self.callback)
		self.pub = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
		self.img_sub = rospy.Subscriber("cozmo_camera/image",Image, self.callback)
		self.bridge = CvBridge()		
		self.start_time = rospy.get_time()
		self.lin_vel = rospy.get_param('~lin_vel',0.2)
        #self.ang_vel = rospy.get_param('~ang_vel',1.5757)

	def callback(self,msg):

		try:
			self.cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
		except CvBridgeError as e:
			rospy.loginfo(e)	
		
		
		(rows,cols,channels) = self.cv_image.shape

		cv2.imshow("Image window", self.cv_image)
		cv2.waitKey(3)

	def _publish_vel(self):
		
		cmd_vel = Twist()
		cmd_vel.linear.x = self.lin_vel
		
		self.pub.publish(cmd_vel)
		
	
	def run(self):

		r = rospy.Rate(20)
		
		while not rospy.is_shutdown():
			self._publish_vel()
			r.sleep()

cozmo_test = TestNode()
cozmo_test.run()
