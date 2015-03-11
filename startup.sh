#!/bin/bash

cleanup()
{
  sudo pkill node
  pkill HPlayer
  pkill python
  return $?
}
 
control_c()
# run if user hits control-c
{
  echo -en "\n*** Goodbye ! ***\n"
  cleanup
  exit $?
}
 
# trap keyboard interrupt (control-c)
trap control_c SIGINT

#initial clean up
cleanup

sudo /usr/local/lib/node_modules/forever/bin/forever start --minUptime 1000 --spinSleepTime 1000 -o /home/pi/griotte/logs/IOInterface.log /home/pi/griotte/IOInterface/IOInterface.js
sudo /usr/local/lib/node_modules/forever/bin/forever start --minUptime 1000 --spinSleepTime 1000 -o /home/pi/griotte/logs/Webserver.log /home/pi/griotte/WebServer/WebServer.js
sudo /usr/local/lib/node_modules/forever/bin/forever start --minUptime 1000 --spinSleepTime 1000 -o /home/pi/griotte/logs/OSCDispatcher.log /home/pi/griotte/OSCDispatcher/OSCDispatcher.js
sudo /usr/local/lib/node_modules/forever/bin/forever start --minUptime 1000 --spinSleepTime 1000 -o /home/pi/griotte/logs/ScenarioPlayer.log /home/pi/griotte/ScenarioPlayer/ScenarioPlayer.js

echo "Starting HPlayer in background\n"
echo "" > /home/pi/griotte/logs/HPlayer.log
/home/pi/griotte/bin/HPlayer/bin/HPlayer > /home/pi/griotte/logs/HPlayer.log 2>&1 &

echo "Starting HDmx in background\n"
echo "" > /home/pi/griotte/logs/HDmx.log
/home/pi/griotte/bin/HDmx/HDmx > /home/pi/griotte/logs/HDmx.log 2>&1 &

echo "Press [CTRL+C] to stop.."
while :
do
	sleep 1
done
