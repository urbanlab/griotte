/* Events Routing */

// LOAD MODULES
var WebServer 		= require('./WebServer/WebServer.js');
//var OSCInterface 	= require('./OSCInterface/OSCInterface.js');
var HPlayer 		= require('./HPlayer');
var MediaManager 	= require('./MediaManager/MediaManager.js');
var ScenarioManager 	= require('./ScenarioManager/ScenarioManager.js');
var ConfigHelper 	= require('./ConfigHelper.js');
var ProcessManager 	= require('./ProcessManager/ProcessManager.js');
//var RemoteInterface = require('./RemoteInterface/RemoteInterface.js');
var SerialInterface = require('./SerialInterface/SerialInterface.js');
var IcePicker = require('./IcePicker.js');

/**
MODULE MANAGER
**/
function ModuleManager(){
	
	this.isRunning 	= false;
	
	this.config			 = ConfigHelper.loadConfig();
	this.webServer		 = new WebServer(this.config.WebServer);
	//this.oscInterface	 = new OSCInterface(this.config.OSCInterface);
	//this.player			 = new HPlayer(this.config.HPlayer);
	//this.mediaManager	 = new MediaManager(this.config.MediaManager);
	//this.scenarioManager	 = new ScenarioManager(this.config.ScenarioManager);
	this.processManager  = new ProcessManager();
	this.serialInterface = new SerialInterface(this.config.SerialInterface);
	this.icePicker = new IcePicker(this.config.IcePicker);
	
	this.link();
	
	this.startupList = [
						/*{
							context:this.mediaManager,
							method:this.mediaManager.loadFromUSBStorage
						},*/
						{
							context:this.mediaManager,
							method:this.mediaManager.updateMediaList // error handling !!
						},
						{
							context:this.scenarioManager,
							method:this.scenarioManager.updateScenarioList // error handling !!
						},
						{	
							context:this,
							method:this.startServices
						}];
}

/**
LINK MODULE EVENTS
**/
ModuleManager.prototype.link = function() {
	
	var self = this;

	/*this.webServer.eventEmitter.on('socketConnection',function(client){	
		client.sendMediaList(self.mediaManager.mediaList);
		client.sendScenarioList(self.scenarioManager.scenarioList);
		client.sendPlayerStatus(self.player.status());
	});*/
	
/*	this.webServer.eventEmitter.on('getScenario',function(client,scenario){	
		//console.log(scenario);
		if(scenario)
			client.sendScenario(self.scenarioManager.getScenario(scenario));
	});*/

/*	this.webServer.eventEmitter.on('createScenario',function(client,scenario){	
		//console.log(scenario);
		if(scenario)
			self.scenarioManager.createScenario(scenario,function(scenariopath,scenariolist){
				client.sendScenarioCreated(scenariopath,scenariolist);
			});
	});*/
	
/*	this.webServer.eventEmitter.on('saveScenario',function(client,data){	
		//console.log(data);
		if(data.scenario && data.scenariopath)
			self.scenarioManager.saveScenario(data.scenariopath,data.scenario,function(scenariopath){
				client.sendScenarioSaved(scenariopath);		
			});
	});*/

/*	this.webServer.eventEmitter.on('deleteScenario',function(client,scenariopath){	
		//console.log(data);
		if(scenariopath)
			self.scenarioManager.deleteScenario(scenariopath,function(scenariolist){
				client.sendScenarioDeleted(scenariolist);		
			});
	});*/	
	
	this.oscInterface.eventEmitter.on('status', function(status){
		//self.player.status(status);
		
		//console.log("osc status received");
		self.webServer.sendPlayerStatus(self.player.status(status));
		// we have a heart beat from the player, we push back the IcePicker
		//self.icePicker.pushBack();
	});
	
/*	this.webServer.eventEmitter.on('play', function(socketId,media){
		if (self.player.loop) self.oscInterface.playloop(media);
		else self.oscInterface.play(media);
		console.log("play  "+media);
	});*/
	
/*	this.webServer.eventEmitter.on('next', function(socketId){
		self.oscInterface.next();	
		console.log("next");
	});*/
	
/*	this.webServer.eventEmitter.on('prev', function(socketId){
		self.oscInterface.prev();	
		console.log("prev");
	});*/
	
/*	this.webServer.eventEmitter.on('pause', function(socketId){
		self.oscInterface.pause();	
		console.log("pause");
	});*/
	
/*	this.webServer.eventEmitter.on('resume', function(socketId){
		self.oscInterface.resume();	
		console.log("resume");
	});*/
	
/*	this.webServer.eventEmitter.on('stop', function(socketId){
		self.oscInterface.stop();
		console.log("stop");
	});*/
	
/*	this.webServer.eventEmitter.on('mute', function(socketId){
		self.oscInterface.mute();
		console.log("mute");
	});*/
	
/*	this.webServer.eventEmitter.on('unmute', function(socketId){
		self.oscInterface.unmute();
		console.log("unmute");
	});*/
	
/*	this.webServer.eventEmitter.on('loop', function(socketId){
		self.oscInterface.loop();
		console.log("loop");
	});*/
	
/*	this.webServer.eventEmitter.on('unloop', function(socketId){
		self.oscInterface.unloop();
		console.log("unloop");
	});*/
	
/*	this.webServer.eventEmitter.on('volume', function(socketId,value){
		self.oscInterface.volume(value);	
		console.log("volume "+value);
	});*/
	
/*	this.webServer.eventEmitter.on('zoom', function(socketId,value){
		self.oscInterface.zoom(value);	
	});*/
	
/*	this.webServer.eventEmitter.on('getStatus', function(){
		self.oscInterface.getStatus();	
		//console.log(self.player.status());
		//self.webServer.sendPlayerStatus(self.player.status());
	});*/
	
/*	this.webServer.eventEmitter.on('quit', function(socketId,value){
		self.stop(0);
		process.exit(0);
	});*/
	
	this.serialInterface.eventEmitter.on('open',function(){
		console.log("serial port open");	
	});
	
	this.webServer.eventEmitter.on('blur', function(socketId,value){
		self.oscInterface.blur(value);	
	});
	
	this.serialInterface.eventEmitter.on('error',function(err){
		console.log("serial port error "+err);	
	});
		
	this.serialInterface.eventEmitter.on('close',function(){
		console.log("serial port closed");	
	});
			
	this.serialInterface.eventEmitter.on('volume',function(value){
		self.oscInterface.volume(value);
	});
	this.serialInterface.eventEmitter.on('blur',function(value){
		self.oscInterface.blur(value);
	});
	
	this.icePicker.eventEmitter.on('rampage',function(value){
		self.processManager.killAll();
		self.processManager.spawn(
		self.config.ProcessManager.HPlayerPath,
		[
			'--name',self.player.name,
			'--volume',self.player.volume,
			'--zoom',self.player.zoom,
			'--blur',self.player.blur,
			'--in',self.config.OSCInterface.clientPort,
			'--out',self.config.OSCInterface.serverPort,
			'--base64',(self.config.OSCInterface.base64Encode)?1:0,
			'--loop',(self.player.loop)?1:0,
			'--ahdmi',(self.player.hdmiAudio)?1:0,
			'--info',(self.player.info)?1:0,
			'--media',(self.config.ModuleManager.playlistAutoLaunch) ? self.mediaManager.mediaDirectory : 'none'
		],
		true,	//re-start if killed
		false);  //pipe stdout to console log
		self.icePicker.start();
	});
}	

/**
START ALL
**/
ModuleManager.prototype.start = function() {	
	
	var self = this;
	
	//START STACK
	function sync(task) 
	{
		if(task) 
		{
			task.method.call(task.context,function(args) {
					return sync(self.startupList.shift());
			});
		} 
		else return ;
	}
	
	sync(self.startupList.shift());
}

/**
START SERVICES
**/
ModuleManager.prototype.startServices = function() {	
	

	//HPLAYER ZOMBIES KILLER
	this.processManager.cleanZombies('HPlayer');

	//WEBSERVER START
	this.webServer.start();	

	//HPlayer START
	this.processManager.spawn(
		this.config.ProcessManager.HPlayerPath,
		[
			'--name',this.player.name,
			'--volume',this.player.volume,
			'--zoom',this.player.zoom,
			'--blur',this.player.blur,
			'--in',this.config.OSCInterface.clientPort,
			'--out',this.config.OSCInterface.serverPort,
			'--base64',(this.config.OSCInterface.base64Encode)?1:0,
			'--loop',(this.player.loop)?1:0,
			'--ahdmi',(this.player.hdmiAudio)?1:0,
			'--info',(this.player.info)?1:0,
			'--media',(this.config.ModuleManager.playlistAutoLaunch) ? this.mediaManager.mediaDirectory : 'none'
		],
		true,	//re-start if killed
		false);  //pipe stdout to console log
		
	
	//SERIAL START
	//this.serialInterface.start();
	
	//ICEPICKER START
	//this.icePicker.start();
	
	console.log('Running..'.green+'\n');
	this.isRunning = true;
}



/**
STOP ALL
**/
ModuleManager.prototype.stop = function() {
	
	if (this.isRunning) 
	{
		this.webServer.stop();
		this.processManager.killAll();
	}
	this.isRunning = false;
}

module.exports = ModuleManager;

