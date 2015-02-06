var Raspiomix = require('./Raspiomix.js');
//var DMXInterface = require('./DMXInterface.js');
var osc = require('node-osc');


var IODeviceAddesses = {
	raspiomix:"raspiomix",
	grovepi:"grovepi",
	arduino:"arduino",
	dmxusbpro:"dmxusbpro"
}
var IOCommands = {
	geta:"getAnalog",
	getd:"getDigital",
	writed:"writeDigital",
	getrtc:"getRtc",
	senddmx:"senddmx",
	senddmxmultiple:"senddmxmultiple",
	senddmxblackout:"senddmxblackout"
}


function IOInterface(){
	
	
	this.raspiomix = new Raspiomix();
	//this.dmxInterface = new DMXInterface();
	
	
	this.url = '127.0.0.1';
	this.clientPort = 5000;
	this.serverPort = 7000;
	this.baseAddress = "iointerface";

	
	var self = this;
	
	//OSC CLIENT: SEND MESSAGES
	this.oscClient = new osc.Client(this.url, this.clientPort); 
	this.oscClient.sendMessageOSC = function(address, args){
		var message = new osc.Message(address);
		if(typeof args !== 'undefined')// we got args
			for(var k=0;k<args.length;k++)// we push args
				message.append(args[k]);
	
		self.oscClient.send(message);	
		
	};
	
	//OSC SERVER: RECEIVE MESSAGES
	this.oscServer = new osc.Server(this.serverPort, this.url);
	this.oscServer.on("message", function(message,rinfo){
			self.receiveMessageOSC(message,rinfo);
	});	
	
	//var handler = this.stayAlive();
}

IOInterface.prototype.stayAlive = function(){
	var self = this;
	return setInterval(function(){
			//console.log('I am still alive');
			self.raspiomix.printStatus();
	},1000);
}


IOInterface.prototype.receiveMessageOSC = function(message,rinfo){	
		console.log(message);
	
		var mes = message.slice();
		var address = mes.shift();
		var addressElements = address.split('/');
		var baseAddress = addressElements.shift();
		var baseAddressElements = baseAddress.split(':');
		var from = baseAddressElements.shift();
		var to = baseAddressElements.shift();
		
		var deviceAddress = addressElements.shift();
		switch(deviceAddress){
				case IODeviceAddesses.raspiomix :
					var command = addressElements.shift();
					switch(command){
						case IOCommands.geta:
							var channel = mes.shift();
							this.oscClient.sendMessageOSC(to+':'+from+'/'+deviceAddress+'/'+'analogValue',[channel,this.raspiomix.getAdc(channel)]);
						break;
						case IOCommands.getd :
							var channel = mes.shift();
							this.oscClient.sendMessageOSC(to+':'+from+'/'+deviceAddress+'/'+'digitalValue',[channel,this.raspiomix.readDigital(this.raspiomix.channelToPin(channel))]);
						break;
						case IOCommands.writed :
							var channel = mes.shift();
							var value = mes.shift();
							this.raspiomix.writeDigital(this.raspiomix.channelToPin(channel),value);
						break;
						case IOCommands.getRtc :
							var channel = mes.shift();
							// nothing for the moment
						break;
						default: console.log("message not recognized: "+ message);	
					}
				break;
				case IODeviceAddesses.grovepi :
					
				break;
				case IODeviceAddesses.arduino :
					
				break;
				case IODeviceAddesses.dmxusbpro :
					
					/*var command = addressElements.shift();
					switch(command){
						case IOCommands.senddmx:
							var channel = mes.shift();
							var value = mes.shift();
							this.dmxInterface.send(channel,value);
						break;
						case IOCommands.senddmxmultiple :
							var valuesString = mes.shift();
							console.log(valuesString);
							this.dmxInterface.sendM(JSON.parse(valuesString));
						break;
						case IOCommands.senddmxblackout :
							this.dmxInterface.blackout();
						break;
						default: console.log("message not recognized: "+ message);	
					}		*/			
				break;				
				default: return console.error("IO Address not recognized : "+baseAddress);
		}
	
}

var iointerface = new IOInterface();

module.exports = IOInterface;

