#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
rosrun pc_controller encoderServer.py
