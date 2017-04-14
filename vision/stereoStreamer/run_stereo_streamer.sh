#!/bin/bash
echo "running left streamer"
screen -d -m -S leftstreamer ~/ECE592_63_IndoorSLAM/FPV/stereoStreamer/run_left.sh
echo "waiting for 20s"
sleep 20
echo "running right streamer"
screen -d -m -S rightstreamer ~/ECE592_63_IndoorSLAM/FPV/stereoStreamer/run_right.sh
