#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
python ../../../vision/stereoReceiver/rosReceiver_synch.py
