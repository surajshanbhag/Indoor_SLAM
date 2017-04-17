#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
rosrun ros_receiver rosReceiver_Right.py 
#python ../../../vision/stereoReceiver/rosReceiver_Right.py ../../../vision/stereoReceiver/right.yaml
