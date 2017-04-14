#!/bin/bash -x
cur_dir="~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts"
echo "starting roscore"
screen -d -m -S roscore ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-roscore.sh
sleep 5
echo "uploading robot description"
screen -d -m -S robot_model ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-description.sh
sleep 5
echo "starting joy node" 
screen -d -m -S joynode ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-joy_node.sh
sleep 5
echo "starting motor control" 
screen -d -m -S motor_control ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-motor_control.sh
sleep 5
echo "starting rosreceiver_left" 
screen -d -m -S rosreceiver_left ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-rosreceiver_left.sh
sleep 5
echo "starting rosreceiver_right" 
screen -d -m -S rosreceiver_right ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-rosreceiver_right.sh
sleep 5
echo "starting rosreceiver_synch" 
screen -d -m -S rosreceiver_synch ~/GIT/ECE592_63_IndoorSLAM/FPV/stereoReceiver/auto_scripts/start-rosreceiver_synch.sh
sleep 5

echo "ALL set to go!"
echo "Check if the comm light is green: else run :  pkill screen   and execute this script again"
