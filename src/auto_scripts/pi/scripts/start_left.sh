#!/bin/bash
source ~/.bashrc
python ../../vision/stereoStreamer/streamer.py --device=/dev/video0 --ip=10.42.0.1 --port=50677 --size=800,600

