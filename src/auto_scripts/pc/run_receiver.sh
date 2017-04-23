#!/bin/bash
echo "starting roscore"
screen -d -m -S roscore ./scripts/start-roscore.sh
sleep 5
echo "starting rosreceiver_left" 
screen -d -m -S rosreceiver_left ./scripts/start-rosreceiver_left.sh
sleep 5
echo "starting rosreceiver_right" 
screen -d -m -S rosreceiver_right ./scripts/start-rosreceiver_right.sh
sleep 5
echo "starting rosreceiver_synch" 
screen -d -m -S rosreceiver_synch ./scripts/start-rosreceiver_synch.sh
echo "ALL set to go!"
rqt &
