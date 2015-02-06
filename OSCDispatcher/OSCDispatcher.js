var osc = require('node-osc');

function OSCDispatcher(config){
	
	var self = this;
	
	this.url = '127.0.0.1';
	this.port = 5000; // server port
	this.server = null;
	
	this.services = [
		{
			name:"hplayer",
			port:9000,
		},
		{
			name:"scenario",
			port:8000
		},
		{
			name:"scenarioplayer",
			port:8001
		},
		{
			name:"iointerface",
			port:7000
		},
		{
			name:"webserver",
			port:6000
		}
	];
	
	this.start();
	//console.log(this);
}

OSCDispatcher.prototype.start = function(){

	var self = this;
	
	this.server = new osc.Server(this.port,this.url);
	this.server.on("message", function(message,rinfo){
			self.receiveMessageOSC(message,rinfo);
	});
	
	for(var k = 0; k<this.services.length; k++){
		this.services[k].client = new osc.Client(this.url,this.services[k].port);
		this.services[k].client.sendMessage = this.sendMessageOSC;
	}
}

OSCDispatcher.prototype.receiveMessageOSC = function(message,rinfo){
	//console.log(message);
	//shallow clone
	var mes = message.slice();
	//console.log(rinfo);
	var address = mes.shift();
	var addressElements = address.split('/');
	var baseAddress = addressElements.shift();
	var baseAddressElements = baseAddress.split(':');
	var from = baseAddressElements.shift();
	var to = baseAddressElements.shift();
	
	// HACK POUR MGR
	/*if(message[0] === "#bundle"){
		var hpmess = message[2];
		hpmess.unshift("hplayer:webserver/status");
		return this.services[4].client.sendMessage(hpmess)
	}*/
	
	var k = 0;
	for(var k = 0; k<this.services.length; k++){
			if(this.services[k].name == to){
				return this.services[k].client.sendMessage(message)
			}
				
	}
	
}
OSCDispatcher.prototype.sendMessageOSC = function(message){
	//console.log(message);
	var address = message.shift();
	this.send(address,message);
}

module.exports = OSCDispatcher;

var oscdispatcher = new OSCDispatcher();