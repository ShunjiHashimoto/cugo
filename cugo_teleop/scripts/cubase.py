#!/usr/bin/env python
# -*- coding: utf-8 -*-

## object_detection_cubase & tele_operation!　##

import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import RPi.GPIO as GPIO
from std_msgs.msg import String

top = 1000
bottom = 50
R = 12
L = 13
ENABLE_r = 17
ENABLE_l = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(L, GPIO.OUT)
GPIO.setup(ENABLE_r, GPIO.OUT)
GPIO.setup(ENABLE_l, GPIO.OUT)
GPIO.output(ENABLE_r, GPIO.LOW)
GPIO.output(ENABLE_l, GPIO.LOW)

p_r = GPIO.PWM(R, bottom)
p_l = GPIO.PWM(L, bottom)

p_r.start(0)
p_l.start(0)

BTN_BACK = 0x0100
BTN_Y = 0x0001
BTN_A = 0x0002
AXS_MAX = 1.0
AXS_OFF = 0.0

class CugoController():
    def __init__(self):
        self.message = "stop"
        self.btn = 0
        self.main = 0
        self.joy_l = 0
        self.joy_r = 0
        self.percent = 80

        # subscribe to motor messages on topic "msg_topic"
        self.str_sub = rospy.Subscriber("/msg_topic", String, self.strCallback, queue_size=1)
        
        # subscribe to joystick messages on topic "joy"
        self.joy_sub = rospy.Subscriber("joy", Joy, self.joyCallback, queue_size=1)
        
    def modeChange(self):
        if self.main == 1:
            ### old_teleop start 
            motor_l = self.joy_l
            motor_r = self.joy_r
            
            time.sleep(0.1)
            
            if motor_l > 0 and motor_r > 0:
                GPIO.output(ENABLE_r, GPIO.LOW)
                GPIO.output(ENABLE_l, GPIO.LOW)
                p_r.ChangeDutyCycle(motor_l)
                p_l.ChangeDutyCycle(motor_r)
                print("go:", motor_l, motor_r)
            
            elif motor_l < 0 and motor_r < 0:
                GPIO.output(ENABLE_r, GPIO.HIGH)
                GPIO.output(ENABLE_l, GPIO.HIGH)
                p_r.ChangeDutyCycle(-(motor_l))
                p_l.ChangeDutyCycle(-(motor_r))
                print("back:", motor_l, motor_r)
            
            else:
                print("stop:", motor_l, motor_r)
                p_r.stop()
                p_l.stop()
                p_r.start(0)
                p_l.start(0)

        elif self.main == 0:
            ### new_teleop start
            if(self.joy_r == -0):
                self.joy_r = 0
            if(self.joy_l == -0):
                self.joy_l = 0

            motor_l = self.joy_l
            motor_r = self.joy_r
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
            
            if motor_l > 0 and motor_r > 0:
                GPIO.output(ENABLE_r, GPIO.LOW)
                GPIO.output(ENABLE_l, GPIO.LOW)
                p_r.ChangeDutyCycle(motor_l)
                p_l.ChangeDutyCycle(motor_r)
                print("go:", motor_l, motor_r)
            
            elif motor_l < 0 and motor_r < 0:
                GPIO.output(ENABLE_r, GPIO.HIGH)
                GPIO.output(ENABLE_l, GPIO.HIGH)
                p_r.ChangeDutyCycle(-(motor_l))
                p_l.ChangeDutyCycle(-(motor_r))
                print("back:", motor_l, motor_r)
            
            else:
                print("stop:", motor_l, motor_r)
                p_r.stop()
                p_l.stop()
                p_r.start(0)
                p_l.start(0)

        else:
            if self.message == "go ahead":
                print("go ahead")
                motor_l = 80.0
                motor_r = 80.0
                GPIO.output(ENABLE_r, GPIO.LOW)
                GPIO.output(ENABLE_l, GPIO.LOW)
                p_r.ChangeDutyCycle(motor_l)
                p_l.ChangeDutyCycle(motor_r)
                
            elif self.message == "turn right":
                print("turn right")
                motor_l = 80.0
                motor_r = 10.0
                GPIO.output(ENABLE_r, GPIO.LOW)
                GPIO.output(ENABLE_l, GPIO.LOW)
                p_r.ChangeDutyCycle(motor_l)
                p_l.ChangeDutyCycle(motor_r)
                
            elif self.message == "turn left":
                print("turn left")
                motor_l = 10.0
                motor_r = 80.0
                GPIO.output(ENABLE_r, GPIO.LOW)
                GPIO.output(ENABLE_l, GPIO.LOW)
                p_r.ChangeDutyCycle(motor_l)
                p_l.ChangeDutyCycle(motor_r)
                
            elif self.message == "stop":
                print("stop")
                p_r.stop()
                p_l.stop()
                p_r.start(0)
                p_l.start(0)
            else:
                print("error")
                #time.sleep(0.1)
    
    def strCallback(self, msg):
        self.message = msg.data
        
    def joyCallback(self, joy_msg):
        newbtn = 0
        
        if(joy_msg.buttons[6]):
            newbtn |= BTN_BACK
        
        joy_l = joy_msg.axes[1]
        if(joy_l <= -AXS_OFF):
            joy_l += AXS_OFF
        elif(joy_l >= AXS_OFF):
            joy_l -= AXS_OFF
        else:
            joy_l = 0
            
        joy_r = joy_msg.axes[4]
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
    GPIO.cleanup()