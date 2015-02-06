/* Main Controller of HP */

//TODO : Store player state reguraly into config
//TODO : Serial interface + patch


var ModuleManager = require('./ModuleManager');
var modules = new ModuleManager(); 

///////////////////////////////////////////////////////////
//START HCONTROLLER
//////////////////////////////////////////////////////////

console.log('\033[2J');
console.log('\n---HController starting---'.green);
modules.start();

///////////////////////////////////////////////////////////
//EXIT
//////////////////////////////////////////////////////////

function exit(code,err) {
    
    console.log(' ');
    
    modules.stop(code);
    
    
	if (code == 2) console.log('Exit on SIGINT'.red);
	else if (code == 99) console.log('Exit on Uncaught Exception: '.red+err);
	else console.log('Exit'.red);
	
	process.exit(code);
}

//process.on('SIGINT', exit.bind(null,2)); //CTRL-C
//process.on('uncaughtException', function (err) { exit(99,err); });









