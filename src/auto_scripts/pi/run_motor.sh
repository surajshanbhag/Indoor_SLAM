#!/bin/bash
sudo v4l2-ctl --set-ctrl=focus_auto=0 --dev=/dev/video1
sudo v4l2-ctl --set-ctrl=focus_absolute=0 --dev=/dev/video1
sudo v4l2-ctl --set-ctrl=focus_auto=0 --dev=/dev/video0
sudo v4l2-ctl --set-ctrl=focus_absolute=0 --dev=/dev/video0

echo "running encoders"
screen -d -m -S encoder ./scripts/start_encoder.sh
echo "running motor"
screen -d -m -S motorcontrol ./scripts/start_motor.sh
