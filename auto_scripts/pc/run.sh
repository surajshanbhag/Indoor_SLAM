#!/bin/bash -x
echo "starting roscore"
screen -d -m -S roscore ./start-roscore.sh
sleep 5
echo "uploading robot description"
screen -d -m -S robot_model ./start-description.sh
sleep 5
echo "starting joy node" 
screen -d -m -S joynode ./start-joy_node.sh
sleep 5
echo "starting motor control" 
screen -d -m -S motor_control ./start-motor_control.sh
sleep 5
echo "starting rosreceiver_left" 
screen -d -m -S rosreceiver_left ./start-rosreceiver_left.sh
sleep 5
echo "starting rosreceiver_right" 
screen -d -m -S rosreceiver_right ./start-rosreceiver_right.sh
sleep 5
echo "starting rosreceiver_synch" 
screen -d -m -S rosreceiver_synch ./start-rosreceiver_synch.sh
sleep 5

echo "ALL set to go!"
echo "Check if the comm light is green: else run :  pkill screen   and execute this script again"
