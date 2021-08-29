#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import Adafruit_PCA9685
from Adafruit_MotorHAT import Adafruit_MotorHAT
import time


mh1 = Adafruit_MotorHAT(addr=0x60)
mh2 = Adafruit_MotorHAT(addr=0x70)
myMotor1 = mh1.getMotor(1)
myMotor2 = mh2.getMotor(2)


def joy_listener():
    # start node
    rospy.init_node("joy_twist", anonymous=True)

    # subscribe to joystick messages on topic "joy"
    rospy.Subscriber("joy", Joy, joy_callback, queue_size=1)

    # keep node alive until stopped
    rospy.spin()

# called when joy message is received
def joy_callback(joy_msg):
    #value_0 = int(joy_msg.axes[0]*255)
    value_1 = int(joy_msg.axes[1]*255)
    #value_3 = int(joy_msg.axes[3]*255)
    value_2 = int(joy_msg.axes[4]*255)
    
    if value_1 == -0:
        value_1 = 0
        
    if value_2 == -0:
        value_2 = 0
    
    if value_1 > 0 and value_2 > 0:
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor1.setSpeed(value_1)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.setSpeed(value_2)
    
    elif value_1 < 0 and value_2 < 0:
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor1.setSpeed(-(value_1))
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.setSpeed(-(value_2))
    
    else:
        myMotor1.run(Adafruit_MotorHAT.RELEASE)
        myMotor2.run(Adafruit_MotorHAT.RELEASE)
    #print(int(value_1))
    #print(int(value_2))

if __name__ == '__main__':
    try:
        joy_listener()
    except rospy.ROSInterruptException:
        pass
