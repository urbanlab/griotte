#!/bin/bash

cleanup()
{
  sudo pkill node
  pkill HPlayer
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

sudo /usr/local/lib/node_modules/forever/bin/forever start -o /home/pi/griotte/logs/Webserver.log /home/pi/griotte/WebServer/WebServer.js
sudo /usr/local/lib/node_modules/forever/bin/forever start -o /home/pi/griotte/logs/OSCDispatcher.log /home/pi/griotte/OSCDispatcher/OSCDispatcher.js
sudo /usr/local/lib/node_modules/forever/bin/forever start -o /home/pi/griotte/logs/ScenarioPlayer.log /home/pi/griotte/ScenarioPlayer/init.js
sudo /usr/local/lib/node_modules/forever/bin/forever start -o l/home/pi/griotte/logs/IOInterface.log /home/pi/griotte/IOInterface/IOInterface.js
echo "Starting HPlayer in background\n"
echo "" > /home/pi/griotte/logs/HPlayer.log
/home/pi/griotte/bin/HPlayer/bin/HPlayer > /home/pi/griotte/logs/HPlayer.log 2>&1 &

echo "Press [CTRL+C] to stop.."
while :
do
	sleep 1
done
