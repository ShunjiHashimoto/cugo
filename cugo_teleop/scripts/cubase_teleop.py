#!/usr/bin/env python
# -*- coding: utf-8 -*-

## object_detection_cubase & tele_operation!　##

import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import String

top = 1000
bottom = 50
R = 12
L = 13
ENABLE_r = 17
ENABLE_l = 18

BTN_BACK = 0x0100
BTN_Y = 0x0001
BTN_A = 0x0002
AXS_MAX = 1.0
AXS_OFF = 0.0
# y = button[3], a = button[0]
class CugoController():
    def __init__(self):
        self.message = "stop"
        self.btn = 0
        self.main = 0
        self.joy_l = 0
        self.joy_r = 0
        self.percent = 50
        self.str_sub = rospy.Subscriber("/msg_topic", String, self.strCallback, queue_size=1)
        self.joy_sub = rospy.Subscriber("joy", Joy, self.joyCallback, queue_size=1)
        
    def modeChange(self):
        if self.main == 0:
            ### old_teleop start 
            print("old_teleop mode")

        elif self.main == 1:
            ### new_teleop start
            print("new_teleop mode")
            if(self.joy_r == -0):
                self.joy_r = 0
            if(self.joy_l == -0):
                self.joy_l = 0

            motor_l = self.joy_l
            motor_r = self.joy_l
            max = self.percent
            ## 右回り
            if(self.joy_r < 0):
                if(self.joy_l > 0):
                    motor_r  += (self.joy_l * self.joy_r)/max
                else:
                    motor_r -= self.joy_r
            ## 左回り
            elif(self.joy_r > 0):
                if(self.joy_l > 0):
                    motor_l -= (self.joy_r * self.joy_l) / max 
                else:
                    motor_l += self.joy_r 
            else:
                motor_l = self.joy_l
                motor_r = self.joy_l

            time.sleep(0.1)
            print("motor_value: motor_l, motor_r", motor_l, motor_r)
            return

        else:
            print("object_detection mode")
    
    def strCallback(self, msg):
        self.message = msg.data
        
    def joyCallback(self, joy_msg):
        newbtn = 0
        
        if(joy_msg.buttons[6]):
            newbtn |= BTN_BACK
        elif(joy_msg.buttons[0]):
            newbtn |= BTN_A
        elif(joy_msg.buttons[3]):
            newbtn |= BTN_Y
        
        joy_l = joy_msg.axes[1]
        if(joy_l <= -AXS_OFF):
            joy_l += AXS_OFF
        elif(joy_l >= AXS_OFF):
            joy_l -= AXS_OFF
        else:
            joy_l = 0
            
        joy_r = joy_msg.axes[3]
        if(joy_r <= -AXS_OFF):
            joy_r += AXS_OFF
        elif(joy_r >= AXS_OFF):
            joy_r -= AXS_OFF
        else:
            joy_r = 0
        
        self.joy_l = int(self.percent * joy_l / (AXS_MAX - AXS_OFF))
        self.joy_r = int(self.percent * joy_r / (AXS_MAX - AXS_OFF))

        push = ((~self.btn) & newbtn)
        self.btn = newbtn
        if(push & BTN_BACK):
            self.main = (self.main + 1)%3
        elif(push & BTN_Y):
            self.percent += 10
        elif(push & BTN_A):
            self.percent -= 10
            
        if(self.percent > 100):
            self.percent = 100
        elif(self.percent < 10):
            self.percent = 10

def main():
    # start node
    rospy.init_node("cubase", anonymous=True)
        
    instance = CugoController()
 
    # ratesleep
    rate = rospy.Rate(40)
    
    while not rospy.is_shutdown():
        instance.modeChange()
        rate.sleep()
        
    # spin
    rospy.spin()
                
if __name__ == '__main__':
    main()
