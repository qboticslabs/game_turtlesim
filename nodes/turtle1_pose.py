#!/usr/bin/env python
#-*-coding:utf-8 -*-
 
import roslib; roslib.load_manifest('game_turtlesim')
import rospy
import time
 
from turtlesim.msg import Pose
 
 
def controller(data):
    
    # запись данных положения turtle1
    rospy.set_param("game_turtlesim/turtle1_pose",[data.x,data.y])
    rospy.loginfo("x="+str(data.x)+" y="+str(data.y))
    # пауза 
    #rospy.sleep(0.1)

def listener():
     rospy.init_node('sub_turtle1_pose')
     # установка параметров
     rospy.set_param("game_turtlesim/turtle1_pose",[0.0, 0.0]) 
    
     sub = rospy.Subscriber("turtle1/pose",Pose,controller)
     rospy.spin()
  
if __name__ == '__main__':
   listener()
