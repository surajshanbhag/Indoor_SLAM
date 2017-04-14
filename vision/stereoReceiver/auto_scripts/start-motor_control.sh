#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
cur_dir=`pwd`
python ~/GIT/ECE592_63_IndoorSLAM/driveControl/src/pcControl/scripts/motorControlServer.py
