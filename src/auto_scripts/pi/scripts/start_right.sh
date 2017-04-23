#!/bin/bash
source ~/.bashrc
python ../../vision/stereoStreamer/streamer.py --device=/dev/video1 --ip=10.42.0.1 --port=50678 --size=800,600
