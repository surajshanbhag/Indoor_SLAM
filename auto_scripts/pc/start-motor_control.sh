#!/bin/bash
source /opt/ros/kinetic/setup.sh
source ~/catkin_ws/devel/setup.bash
python ../../control/pcControl/scripts/motorControlServer.py
