#!/usr/bin/env python
#-*-coding:utf-8 -*-

import roslib; roslib.load_manifest('game_turtlesim')
import rospy
import math
import random
import time

from std_msgs.msg import String
from turtlesim.srv import TeleportRelative
#from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
from turtlesim.srv import Kill

K_ANGLE=8.0
K_SPEED=2.0
T_SPEED=5.0

def talker():
    rospy.init_node('turtle1_go')
    serv1=rospy.ServiceProxy('turtle1/teleport_relative',TeleportRelative)
    rospy.set_param("game_turtlesim/time",0)
    rospy.set_param("game_turtlesim/count",0)
    rospy.set_param("game_turtlesim/count_turtles",0)
    rospy.set_param("game_turtlesim/list_turtles",[0,0,0,0,0,0,0,0,0,0]) 
    rospy.set_param("game_turtlesim/coord_turtles",[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]) 
    serv2=rospy.ServiceProxy('spawn',Spawn)
    serv3=rospy.ServiceProxy('kill',Kill)
    while not rospy.is_shutdown():
       # движение turtle1
       if rospy.get_param("game_turtlesim/start")==1:
          joy_tek=rospy.get_param("game_turtlesim/joy_tek")
          speed=joy_tek[1]/K_SPEED
          k=1
          if joy_tek[1]<0:
            k=-1
          angle=math.asin(joy_tek[0]*k)/K_ANGLE
          res1=serv1(speed,angle);
       rospy.sleep(0.1)
       # создание черепах turtle00-turtle010
       count_turtles=rospy.get_param("game_turtlesim/count_turtles")
       count=rospy.get_param("game_turtlesim/count")
       if rospy.get_param("game_turtlesim/start")==1 and count_turtles<10 and time.time()-rospy.get_param("game_turtlesim/time")>(T_SPEED-max(2,count*0.03)):
          count_turtles=count_turtles+1
          list_turtles=rospy.get_param("game_turtlesim/list_turtles")
          coord_turtles=rospy.get_param("game_turtlesim/coord_turtles")
          ind=list_turtles.index(0,0,10)
          prv1=False
          while prv1==False:
            x=random.randrange(5,110,5)
            y=random.randrange(5,110,5)
            theta=0.1*random.randint(1,10)
            tek_turtle="turtle0"+str(ind)
            res2=serv2(0.1*x,0.1*y,theta,tek_turtle);
            rospy.loginfo("create turtle="+tek_turtle)
            list_turtles[ind]=1
            coord_turtles[ind]=[x,y]
            rospy.loginfo(list_turtles)
            rospy.set_param("game_turtlesim/list_turtles",list_turtles) 
            rospy.set_param("game_turtlesim/coord_turtles",coord_turtles) 
            rospy.set_param("game_turtlesim/time",time.time())
            rospy.set_param("game_turtlesim/count_turtles",count_turtles)
            prv1=True
       # проверка столкновения turtle1 с turtle00-turtle010
       count=rospy.get_param("game_turtlesim/count")
       list_turtles=rospy.get_param("game_turtlesim/list_turtles")
       coord_turtles=rospy.get_param("game_turtlesim/coord_turtles")
       xy=rospy.get_param("game_turtlesim/turtle1_pose")
       count_turtles=rospy.get_param("game_turtlesim/count_turtles")
       x1=int(xy[0]*10)
       y1=int(xy[1]*10)
       i=0
       for xy in coord_turtles:
          if abs(xy[0]-x1)<4 and abs(xy[1]-(110-y1))<4 and list_turtles[i]==1:
             turtle_del="turtle0"+str(i)
             rospy.loginfo(str(xy[0])+" "+str(xy[1])+" "+str(x1)+" "+str(y1)+" "+turtle_del)
             res3=serv3(turtle_del);
             list_turtles[i]=0
             coord_turtles[i]=[0,0]
             count_turtles=count_turtles-1
             rospy.set_param("game_turtlesim/count",count+1) 
             rospy.set_param("game_turtlesim/count_turtles",count_turtles) 
             rospy.set_param("game_turtlesim/list_turtles",list_turtles) 
             rospy.set_param("game_turtlesim/coord_turtles",coord_turtles) 
          i=i+1       
       

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass

