var vm = require('vm');
var ScenarioAPI = require('./ScenarioAPI.js');
var ScenarioOSC = require('./ScenarioOSC.js');


function Runner(){
	//console.log(process.argv[2]);
	this.scenarioOSC = new ScenarioOSC();
	this.script = vm.createScript(process.argv[2]); 
	this.context = vm.createContext(new ScenarioAPI(this.scenarioOSC));
}

Runner.prototype.run = function(){
	this.script.runInContext(this.context);
	//console.log("finito");
}
var runner = new Runner();
runner.run();