#!/bin/bash
echo "running left streamer"
screen -d -m -S leftstreamer ~/Indoor_SLAM/vision/stereoStreamer/run_left.sh
echo "waiting for 20s"
sleep 20
echo "running right streamer"
screen -d -m -S rightstreamer ~/Indoor_SLAM/vision/stereoStreamer/run_right.sh
