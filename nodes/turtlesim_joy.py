#!/usr/bin/env python
#-*-coding:utf-8 -*-
 
import roslib; roslib.load_manifest('game_turtlesim')
import rospy
import time
 
from sensor_msgs.msg import Joy
import std_srvs.srv 
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportAbsolute
 
 
def controller(data):
    
    # запись данных с джойстиков
    rospy.loginfo(str(data.axes[0])+" "+str(data.axes[3]))
    joy_tek=rospy.get_param("game_turtlesim/joy_tek")
    joy_tek[0]=data.axes[0]
    joy_tek[1]=data.axes[3]
    rospy.set_param("game_turtlesim/joy_tek",joy_tek)
    # проверка takeoff - кнопка start/10
    if(data.buttons[1]==1):  #  B2
        rospy.loginfo("button B2")
        rospy.set_param("game_turtlesim/start",0)
        serv1=rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
        res1=serv1(0.0,0.0,0.89);
    elif(data.buttons[0]==1):  # кнопка A1
        rospy.loginfo("button A1")
        rospy.set_param("game_turtlesim/start",1)
    else:             
        pass
def listener():
     rospy.init_node('sub_turtle1_joy')
     # установка параметров
     rospy.set_param("game_turtlesim/start",1)
     rospy.set_param("game_turtlesim/joy_tek",[0.0, 0.0]) 
     # установить цвет фона
     rospy.set_param("background_r",255)
     rospy.set_param("background_g",255)
     rospy.set_param("background_b",0)
     serv1=rospy.ServiceProxy('/clear',std_srvs.srv.Empty)
     res1=serv1();
     # установить цвет карандаша для turtle1
     serv1=rospy.ServiceProxy('/turtle1/set_pen',SetPen)
     res1=serv1(255,255,0,10,0);
     # черепаху в начальную позицию
     serv1=rospy.ServiceProxy('turtle1/teleport_absolute',TeleportAbsolute)
     res1=serv1(0.0,0.0,0.89);
     # пауза - отдышаться перед игрой
     rospy.sleep(1.0)
    
     sub = rospy.Subscriber("joy",Joy,controller)
     rospy.spin()
  
if __name__ == '__main__':
   listener()
