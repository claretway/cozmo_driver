#! /usr/bin/env python3.5

import rospy
import cozmo
import numpy as np
import sys
import time
import cv2
from PIL import Image, ImageDraw, ImageFont
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import BatteryState
from sensor_msgs.msg import Image as img
from std_msgs.msg import String

_clock_font = None
try:
	_clock_font = ImageFont.truetype("arial.ttf", 100)
except IOError:
	try:
		_clock_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 100)
	except IOError:
		pass

class TestNode(object): 

	def __init__(self, queue_size=100):
		rospy.init_node('test')
		self.sub = rospy.Subscriber("/cozmo/battery",BatteryState, self.callback)
		self.pub = rospy.Publisher("voltage_message_clare",String,queue_size=10)
		#self.imgsub = rospy.
		cozmo.robot.Robot.drive_off_charger_on_connect = False  # Cozmo can stay on his charger for this example
		#cozmo.run_program(self.display_voltage)
		
		

	def callback(self,msg):
		v = msg.voltage
		#rospy.loginfo("Voltage: {}".format(v))
		self.pub.publish(String("{}".format(v)))

	



	"""
	def make_text_image(self, text_to_draw,x,y,font=None):
		text_image = Image.new('RGBA', cozmo.oled_face.dimensions(), (0, 0, 0, 255))

		# get a drawing context
		dc = ImageDraw.Draw(text_image)

		# draw the text
		dc.text((x, y), text_to_draw, fill=(255, 255, 255, 255), font=font)

		return text_image
	"""

	def get_in_position(self, robot: cozmo.robot.Robot):
	    '''If necessary, Move Cozmo's Head and Lift to make it easy to see Cozmo's face'''
	    if (robot.lift_height.distance_mm > 45) or (robot.head_angle.degrees < 40):
	        with robot.perform_off_charger():
	            lift_action = robot.set_lift_height(0.0, in_parallel=True)
	            head_action = robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE,
	                                               in_parallel=True)
	            lift_action.wait_for_completed()
	            head_action.wait_for_completed()

	"""
	def display_voltage(self, robot: cozmo.robot.Robot):

		self.get_in_position(robot)

		while True:
			#current_time = datetime.datetime.now().time()
			time_text = time.strftime("%I:%M:%S %p") 
			voltage_text = '%.2f' % robot.battery_voltage
			time_voltage_text = time_text + '\n' + voltage_text + 'V'

			if robot.battery_voltage < 3.5:
				time_voltage_text = time_voltage_text + ' > Low battery!!'
			else:
				time_voltage_text = time_voltage_text + ' > We good!!'
			
			clock_image = self.make_text_image(time_voltage_text,8,6,_clock_font)
			oled_face_data = cozmo.oled_face.convert_image_to_screen_data(clock_image)
			robot.display_oled_face_image(oled_face_data, 1000.0)
			time.sleep(0.1)
	"""

	@staticmethod
	def run():
		rospy.spin()

cozmo_test = TestNode()
cozmo_test.run()
