var osc = require('node-osc');
var events = require('events');

function ScenarioOSC(config){
	
	var self = this;
	
	this.url = '127.0.0.1';
	this.clientPort = 5000;
	this.serverPort = 8001;
	
	this.services = {
		webserver:"webserver"
	}
	
	this.eventEmitter = new events.EventEmitter();
	
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
			self.receiveMessageOSC(message,rinfo,self.eventEmitter);
	});	
	
	
}

ScenarioOSC.prototype.receiveMessageOSC = function(message,rinfo,eventEmitter){
		
	//console.log(message);
	
	var mes = message.slice();
	var address = mes.shift();
	var addressElements = address.split('/');
	var baseAddress = addressElements.shift();
	var baseAddressElements = baseAddress.split(':');
	var from = baseAddressElements.shift();
	var to = baseAddressElements.shift();
		
	switch(from){
			case this.services.webserver :
						var command = addressElements.shift();
						switch(command){
							case "play" :
								var scenarioname = mes.shift();
								//sketchy
								var scenario = mes.join("");
								
								eventEmitter.emit('play',scenarioname,scenario,from);
							break;
							case "stop" :
								eventEmitter.emit('stop',from);
							break;
							case "getStatus" :
								eventEmitter.emit('status',from);
							break;
							default: console.log("message not recognized: "+ message);	
						}	
			break;
			default: return console.error("Address not recognized : "+baseAddress);
	}

}

ScenarioOSC.prototype.sendStatus = function(to,status){
	this.oscClient.sendMessage("scenarioplayer:"+to,"status",[JSON.stringify(status)])
}

module.exports = ScenarioOSC;