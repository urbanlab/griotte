var osc = require('node-osc');
var events = require('events');
var HPlayer = require('../HPlayer.js');


function OSCInterface(config){
	
	var self = this;
	
	if(typeof config === 'undefined')
		return console.log("no config found for OSCInterface");
	
	this.url = typeof config.url !== 'undefined' ? config.url : '127.0.0.1';
	this.clientPort = typeof config.clientPort !== 'undefined' ? config.clientPort : 5000;
	this.serverPort = typeof config.serverPort !== 'undefined' ? config.serverPort : 6000;
	this.baseAddress = typeof config.baseAddress !== 'undefined' ? config.baseAddress : "";
	this.base64Encode = typeof config.base64Encode !== 'undefined' ? config.base64Encode : false;

	this.services = {
		iointerface:"iointerface",
		hplayer:"hplayer",
		scenarioplayer:"scenarioplayer"
	}
	
	this.eventEmitter = new events.EventEmitter();
	
	//OSC CLIENT: SEND MESSAGES
	this.oscClient = new osc.Client(this.url, this.clientPort); 
	this.oscClient.sendMessage = function (address,operation,args){
		var message = new osc.Message(address+'/'+operation);
		if(typeof args !== 'undefined')// we got args
			for(var k=0;k<args.length;k++)// we push args
				message.append(args[k]);
	
		self.oscClient.send(message);	
	}
	//OSC SERVER: RECEIVE MESSAGES
	this.oscServer = new osc.Server(this.serverPort, this.url);
	this.oscServer.on("message", function(message,rinfo){
			self.receiveMessageOSC(message,rinfo);
	});
//	this.oscServer.on("message", function (message, rinfo) {
//	});
}
OSCInterface.prototype.receiveMessageOSC = function(message,rinfo){
	
	//console.log(message);
	
	var mess = message.slice();
	var address = mess.shift();
	var addressElements = address.split('/');
	var baseAddress = addressElements.shift();
	var baseAddressElements = baseAddress.split(':');
	var from = baseAddressElements.shift();
	var to = baseAddressElements.shift();
	
	switch(from){
			case this.services.scenarioplayer :
				var command = addressElements.shift();
					switch(command){
						case "status":
							this.eventEmitter.emit('spStatus',mess);
						break;
					}
			break;
			case this.services.iointerface :
			break;
			case this.services.hplayer :
				var command = addressElements.shift();
				switch(command){
					case "status":
						var player = new HPlayer();
						player.name = mess.shift();
						switch(mess.shift()){
							case "playing" :
								player.isPlaying = true;
								player.isPaused = false;
							break;
							case "paused" :
								player.isPlaying = true;
								player.isPaused = true;
							break;
							
							case "stoped" : 
								player.isPlaying = false;
								player.isPaused = false;
							break;
			
						}
						/*if(self.base64Encode)
							player.media.filepath = new Buffer(mess.shift(), 'base64').toString('utf8');
						else*/
							player.media.filepath = mess.shift();
						
						player.media.progress = mess.shift();
						player.media.duration = mess.shift();
						player.loop = (mess.shift() === 1);
						player.volume = mess.shift();
						player.isMuted = (mess.shift() === "muted");
						player.zoom = mess.shift();
						player.blur = mess.shift();
						//pb with self ?
						this.eventEmitter.emit('status',player.status());
					break;
					case "ended" :
						// nothing for the moment
					break;
					case "looped" :
						// nothing for the moment
					break;
					default: console.log("message not recognized: "+message);	
				}
			break;				
			default: return console.error("Address not recognized : "+baseAddress);
	}	
	//var args = message.slice();
	//var command = "";	
		
	//Support for direct OSC Message and simple Bundle (with only one message inside)
	/*while (((typeof command !== 'string') || (command.charAt(0) != "/")) && (args.length > 0))
	{
		command = args.shift();
		while(Object.prototype.toString.call(command) === '[object Array]' ) 
		{
			args = command.slice();
			command = args.shift();
		}
	}*/
	
	
}
/***************************   OSCInterface Commands   ************************/


OSCInterface.prototype.quit = function(){
	this.oscClient.sendMessage('quit');
}

//MEDIA LIST 
OSCInterface.prototype.mediaOSCList = function(media){
	if(this.base64Encode){
		if(typeof media === "object"){// allow list of media
			for( var k=0;k<media.length;k++){
				media[k] = new Buffer(media[k]).toString('base64');
			}
		}else
			media = new Buffer(media).toString('base64');
	}
	return (typeof media === "string") ? [media] : media;
}

// scenario player controls
OSCInterface.prototype.playScenario = function(scenarioname,scenario){
	this.oscClient.sendMessage('webserver:scenarioplayer','play',[scenarioname,scenario]);
}
OSCInterface.prototype.stopScenario = function(){
	this.oscClient.sendMessage('webserver:scenarioplayer','stop');
}
// media player controls 
OSCInterface.prototype.play = function(media){
	this.oscClient.sendMessage('webserver:hplayer','play',this.mediaOSCList(media));
}
OSCInterface.prototype.playloop = function(media){
	this.oscClient.sendMessage('webserver:hplayer','playloop',this.mediaOSCList(media));	
}
OSCInterface.prototype.stop = function(){
	this.oscClient.sendMessage('webserver:hplayer','stop');
}
OSCInterface.prototype.next = function(){
	this.oscClient.sendMessage('webserver:hplayer','next');
}
OSCInterface.prototype.prev = function(){
	this.oscClient.sendMessage('webserver:hplayer','prev');
}
OSCInterface.prototype.pause = function(){
	this.oscClient.sendMessage('webserver:hplayer','pause');
}
OSCInterface.prototype.resume = function(){
	this.oscClient.sendMessage('webserver:hplayer','resume');
}
OSCInterface.prototype.loop = function(){
	this.oscClient.sendMessage('webserver:hplayer','loop');
}
OSCInterface.prototype.unloop = function(){
	this.oscClient.sendMessage('webserver:hplayer','unloop');	
}
OSCInterface.prototype.zoom = function(value){
	this.oscClient.sendMessage('webserver:hplayer','zoom',[value]);
}
// SOUND
OSCInterface.prototype.volume = function(value){
	//console.log("volume = "+value);
	this.oscClient.sendMessage('webserver:hplayer','volume',[value]);
}
OSCInterface.prototype.mute = function(){
	this.oscClient.sendMessage('webserver:hplayer','mute');
}
OSCInterface.prototype.unmute = function(){
	this.oscClient.sendMessage('webserver:hplayer','unmute');	
}
// EFFECTS
OSCInterface.prototype.blur = function(blurSize){
	this.oscClient.sendMessage('webserver:hplayer','blur',[blurSize]);
}
// PLAYERS STATUS REQUEST
OSCInterface.prototype.getPlayerStatus = function(){
	//console.log("status asked");
	this.oscClient.sendMessage('webserver:hplayer','getStatus');
}
OSCInterface.prototype.getScenarioPlayerStatus = function(){
	//console.log("status asked");
	this.oscClient.sendMessage('webserver:scenarioplayer','getStatus');
}

module.exports = OSCInterface




