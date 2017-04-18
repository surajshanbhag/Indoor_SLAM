#!/bin/bash -x
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash 
roslaunch rtabmap_ros stereo_mapping.launch
