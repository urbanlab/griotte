var Args = require("arg-parser"),
		fs = require('fs'),
		path = require('path'),
		ScenarioPlayerOSC = require('./ScenarioPlayerOSC.js'),
		ProcessManager 	= require('../ProcessManager/ProcessManager.js');
		

function ScenarioPlayer(){
	
	var self = this;
	
	this.status = {
		isPlaying:false,
		nowplaying:""
	}
	
	var configJSON = fs.readFileSync(__dirname +"/scenarioplayer.config");
	if(typeof configJSON === 'undefined')
		return error.log("no config found for ScenarioPlayer");
	var config = JSON.parse(configJSON);
	
	this.autoplay = typeof config.autoplay !== 'undefined' ? config.autoplay : false;
	this.autoplaysco = typeof config.autoplaysco !== 'undefined' ? config.autoplaysco : "";
	
	this.processManager = new ProcessManager();
	
	this.scenarioPlayerOSC = new ScenarioPlayerOSC();
	this.scenarioPlayerOSC.eventEmitter.on('play', function(scenarioname,scenario,from){
		//var sco = this.openSCO(this.options.input);
		console.log("play ! - "+scenarioname+'\n'+scenario);
		self.play(scenario);
		self.status.nowplaying = scenarioname;
		self.scenarioPlayerOSC.sendStatus(from,self.status)
	});
	this.scenarioPlayerOSC.eventEmitter.on('stop', function(from){
		self.stop();
		self.status.nowplaying = "";
		self.scenarioPlayerOSC.sendStatus(from,self.status);
		// temporary
		self.scenarioPlayerOSC.oscClient.sendMessage("scenarioplayer:iointerface/arduino","resetAll");
	});
	this.scenarioPlayerOSC.eventEmitter.on('status', function(from){
		self.scenarioPlayerOSC.sendStatus(from,self.status)
	});
	
	this.currentScenario = "";

	this.options = this.parseArgs();
	//console.log(this.options);
	if(config.autoplay){
		var sco = this.openSCO(config.autoplaysco);
		if(!sco)
			return error.log("could not open auto play sco");
		this.status.nowplaying = sco.name;
		this.play(sco.codejs);
	}else if(this.options.input){
		var sco = this.openSCO(this.options.input);
		if(!sco)
			return;
		this.status.nowplaying = sco.name;
		//var script = vm.createScript(sco.codejs);
		this.play(sco.codejs);
		
	}
	

	
}


ScenarioPlayer.prototype.parseArgs = function(){
	
	var args = new Args('Scenario Player', '0.0.1','\n','\n\n'); 
	args.add({ name: 'input', desc: 'input file', switches: [ '-i', '--input-file'], value: 'input', required:false });
	args.add({ name: 'verbose', desc: 'verbose mode', switches: [ '-V', '--verbose'] });
	//args.add({ name: 'text', desc: 'text to store', required: false });
	
	//if (args.parse()) console.log(args.params);
	args.parse();
	
	return {input:args.params.input}	
	
}

ScenarioPlayer.prototype.play = function(scenario){
	if(!this.status.isPlaying){
		this.processManager.spawn("node",["/home/pi/griotte/ScenarioPlayer/Runner.js",scenario],false,true); 
		this.status.isPlaying = true;
	}
	
	//var self = this;
	//setTimeout(function(){
	//	self.stop();	
	//},15000);
}


ScenarioPlayer.prototype.stop = function(){
	this.processManager.killAll();
	this.status.isPlaying = false;
}

ScenarioPlayer.prototype.openSCO = function(file){
	
	if(path.extname(file) != ".sco")
		return console.error("\x1B[31m input is not a .sco file\x1B[39m");
	
	var scoFile = fs.readFileSync(file);
	
	return JSON.parse(scoFile);
}

var scenarioPlayer = new ScenarioPlayer();

module.exports = ScenarioPlayer;


