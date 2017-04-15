#!/bin/bash

v4l2-ctl -c focus_auto=0
echo "running left streamer"
screen -d -m -S leftstreamer ~/Indoor_SLAM/auto_scripts/pi/run_left.sh
echo "waiting for 20s"
sleep 20
echo "running right streamer"
screen -d -m -S rightstreamer ~/Indoor_SLAM/auto_scripts/pi/run_right.sh
echo "running encoders"
screen -d -m -S encoder ~/Indoor_SLAM/auto_scripts/pi/run_encoder.sh
echo "running motor"
screen -d -m -S motorcontrol ~/Indoor_SLAM/auto_scripts/pi/run_motor.sh
