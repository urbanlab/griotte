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

forever start -o logs/Webserver.log WebServer/WebServer.js
forever start -o logs/OSCDispatcher.log OSCDispatcher/OSCDispatcher.js
forever start -o logs/ScenarioPlayer.log ScenarioPlayer/init.js
sudo forever start -o logs/IOInterface.log IOInterface/IOInterface.js
echo "Starting HPlayer in background\n"
echo "" > logs/HPlayer.log
bin/HPlayer/bin/HPlayer > logs/HPlayer.log 2>&1 &

echo "Press [CTRL+C] to stop.."
while :
do
	sleep 1
done
