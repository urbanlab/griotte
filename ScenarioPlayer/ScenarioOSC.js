var osc = require('node-osc');

function ScenarioOSC(config){
	
	var self = this;
	
	this.url = '127.0.0.1';
	this.clientPort = 5000;
	this.serverPort = 8000;
	
	this.services = {
		iointerface:"iointerface",
		hplayer:"hplayer"
	}
	
	
	//OSC CLIENT: SEND MESSAGES
	this.oscClient = new osc.Client(this.url, this.clientPort); 
	this.oscClient.sendMessage = function(address,operation, args){
		var message = new osc.Message(address+'/'+operation);
		if(typeof args !== 'undefined')// we got args
			for(var k=0;k<args.length;k++)// we push args
				message.append(args[k]);
		//console.log(message);
		self.oscClient.send(message);	
		
	};
	//OSC SERVER: RECEIVE MESSAGES
	this.oscServer = new osc.Server(this.serverPort, this.url);
	this.oscServer.on("message", function(message,rinfo){
			self.receiveMessageOSC(message,rinfo);
	});	
	
	
	this.cbfifos = {
			digital:{
				IO0:[],
				IO1:[],
				IO2:[],
				IO3:[],
				DIP0:[],
				DIP1:[]
			},
			analog:{
				0:[],
				1:[],
				2:[],
				3:[]
			},
			fdigital:{
				0:[],
				1:[],
				2:[],
				3:[],
				4:[],
				5:[],
				6:[],
				7:[],
				8:[],
				9:[],
				10:[],
				11:[],
				12:[],
				13:[]
			},
			fanalog:{
				0:[],
				1:[],
				2:[],
				3:[],
				4:[],
				5:[]
			}
	};
	
	/*setInterval(function(){
			self.printFifos();
	},100);*/
	
}

ScenarioOSC.prototype.receiveMessageOSC = function(message,rinfo){
		
	//console.log(message);
	
		/*var args = message.slice();
		var address = args.shift();
		var addressElements = address.split('/');
		
		var baseAddress = addressElements[0];*/
	var mes = message.slice();
	var address = mes.shift();
	var addressElements = address.split('/');
	var baseAddress = addressElements.shift();
	var baseAddressElements = baseAddress.split(':');
	var from = baseAddressElements.shift();
	var to = baseAddressElements.shift();
		
	switch(from){
			case this.services.iointerface :
					var deviceAddress = addressElements.shift();
					switch(deviceAddress){
						case "raspiomix" :
							var command = addressElements.shift();
							switch(command){
								case "digitalValue" :
									var channel = mes.shift();
									var value = mes.shift();
									var callback = this.cbfifos.digital[channel].shift();
									callback(value);
								break;
								case "analogValue" :
									var channel = mes.shift();
									var value = mes.shift();
									var callback = this.cbfifos.analog[channel].shift();
									callback(value);
								break;
								default: console.log("message not recognized: "+ message);	
							}	
						break;
						case "grovepi" :
						break;
						case "arduino" :
							var command = addressElements.shift();
							switch(command){
								case "digitalValue" :
									var pin = mes.shift();
									var value = mes.shift();
									// trouver un meilleur system pour firmata
									var callback = this.cbfifos.fdigital[pin][0];
									callback(value);
								break;
								case "analogValue" :
									var pin = mes.shift();
									var value = mes.shift();
									var callback = this.cbfifos.fanalog[pin][0];
									callback(value);
								break;
								default: console.log("message not recognized: "+ message);	
							}
						break;
						default: console.log("device not recognized: "+ message);	
					}	
			break;
			case this.services.hplayer :
				
			break;				
			default: return console.error("Address not recognized : "+baseAddress);
	}

}



/***************************   IOInterface Commands   ************************/

// RASPIOMIX

ScenarioOSC.prototype.getDigital = function(channel,callback){
	this.cbfifos.digital[channel].push(callback);
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/raspiomix','getDigital',[channel]);
	
}
ScenarioOSC.prototype.writeDigital = function(channel,value){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/raspiomix','writeDigital',[channel,value]);
}
ScenarioOSC.prototype.getAnalog = function(channel,callback){	
	this.cbfifos.analog[channel].push(callback);
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/raspiomix','getAnalog',[channel]);
}

// ARDUINO - FIRMATA

ScenarioOSC.prototype.fgetDigital = function(pin,callback){
	this.cbfifos.fdigital[pin].push(callback);
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/arduino','getDigital',[pin]);
	
}
ScenarioOSC.prototype.fwriteDigital = function(pin,value){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/arduino','writeDigital',[pin,value]);
}
ScenarioOSC.prototype.fgetAnalog = function(pin,callback){	
	this.cbfifos.fanalog[pin].push(callback);
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/arduino','getAnalog',[pin]);
}
ScenarioOSC.prototype.fwriteServo = function(pin,value){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/arduino','writeServo',[pin,value]);

}
ScenarioOSC.prototype.fwritePWM = function(pin,value){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/arduino','writePWM',[pin,value]);
}

ScenarioOSC.prototype.printFifos = function(){
	console.log('\x1b[2J\x1b[H');
	console.log('--------- F I F O S ------------');
 	console.log("IO0 : "+this.cbfifos.digital.IO0.length);
 	console.log("IO1 : "+this.cbfifos.digital.IO1.length);
 	console.log("IO2 : "+this.cbfifos.digital.IO2.length);
 	console.log("IO3 : "+this.cbfifos.digital.IO3.length);
 	console.log("DIP0 : "+this.cbfifos.digital.DIP0.length);
 	console.log("DIP1 : "+this.cbfifos.digital.DIP1.length);
 	console.log("AN 0 :"+this.cbfifos.analog[0].length);
 	console.log("AN 1 :"+this.cbfifos.analog[0].length);
 	console.log("AN 2 :"+this.cbfifos.analog[0].length);
 	console.log("AN 3 :"+this.cbfifos.analog[0].length);
}

/***************************   HPlayer Commands   ************************/

ScenarioOSC.prototype.play = function(media){
	this.oscClient.sendMessage("scenario:"+this.services.hplayer,'play',[media]);
}
ScenarioOSC.prototype.playloop = function(media){
	this.oscClient.sendMessage("scenario:"+this.services.hplayer,'playloop',[media]);	
}
ScenarioOSC.prototype.stop = function(){
	this.oscClient.sendMessage("scenario:"+this.services.hplayer,'stop');
}
ScenarioOSC.prototype.pause = function(){
	this.oscClient.sendMessage("scenario:"+this.services.hplayer,'pause');
}
ScenarioOSC.prototype.resume = function(){
	this.oscClient.sendMessage("scenario:"+this.services.hplayer,'resume');
}

/***************************  DMX Commands  ************************/

ScenarioOSC.prototype.sendDmx = function(channel,value){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/dmxusbpro','senddmx',[channel,value]);
}

ScenarioOSC.prototype.sendDmxM = function(valuesString){
	this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/dmxusbpro','senddmxmultiple',[valuesString]);
}
ScenarioOSC.prototype.sendDmxBlackout = function(){
		this.oscClient.sendMessage("scenario:"+this.services.iointerface+'/dmxusbpro','senddmxblackout');

}

module.exports = ScenarioOSC;