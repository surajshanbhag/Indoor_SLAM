#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
#rosrun ros_receiver rosReceiver_synch.py 
python ../../vision/stereoReceiver/ros_receiver/scripts/rosReceiver_synch.py
