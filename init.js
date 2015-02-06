// debug top -p `pgrep node | tr "\\n" "," | sed 's/,$//'`

var ProcessManager 	= require('./ProcessManager/ProcessManager.js');
pm = new ProcessManager();

pm.cleanZombies('HPlayer');
printBlue("starting HPlayer...");
pm.spawn("./bin/HPlayer/bin/HPlayer",[],true,false);

printBlue("starting ScenarioPlayer...");
pm.spawn("node",["./ScenarioPlayer/init.js"],true,false);

printBlue("starting OSCDispatcher...");
pm.spawn("node",["./OSCDispatcher/OSCDispatcher.js"],true,true);

printBlue("starting Webserver...");
pm.spawn("node",["./WebServer/WebServer.js"],true,false);

//printBlue("starting IOInterface...");
//pm.spawn("sudo",["node","./IOInterface/IOInterface.js"],true,true);


process.on('SIGINT', gameover);
process.on('uncaughtException', gameover);
process.on('exit', gameover);
function gameover(code){
	pm.cleanZombies('HPlayer');
	pm.cleanZombies('node');
	//pm.killAll();
	//process.exit(0);
}

function printBlue(what){
	console.log("\x1B[34m"+what+"\x1B[39m");
}