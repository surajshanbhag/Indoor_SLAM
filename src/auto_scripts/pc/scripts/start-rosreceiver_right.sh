#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
#rosrun ros_receiver rosReceiver_Left.py 
python ../../vision/stereoReceiver/ros_receiver/scripts/rosReceiver.py --calibration=../../vision/stereoReceiver/right.yaml --port=50678 --side=right --link=camera_right_link
