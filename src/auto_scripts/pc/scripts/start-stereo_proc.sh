#!/bin/bash -x
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash 
ROS_NAMESPACE=stereo rosrun stereo_image_proc stereo_image_proc
