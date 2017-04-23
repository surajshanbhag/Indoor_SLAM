#!/bin/bash
echo "starting roscore"
screen -d -m -S roscore ./scripts/start-roscore.sh
sleep 5
echo "uploading robot description"
screen -d -m -S robot_model ./scripts/start-description.sh
sleep 5
echo "starting joy node" 
screen -d -m -S joynode ./scripts/start-joy_node.sh
sleep 5
echo "starting motor control" 
screen -d -m -S motor_control ./scripts/start-motor_control.sh
sleep 5
echo "starting encoder " 
screen -d -m -S encoder ./scripts/start-encoder.sh

echo "ALL set to go!"

