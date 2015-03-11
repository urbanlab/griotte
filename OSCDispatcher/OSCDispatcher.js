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
			postmanTag: true
		},
		{
			name:"hdmx",
			port:3000,
			postmanTag: false
		},
		{
			name:"scenario",
			port:8000,
			postmanTag: true
		},
		{
			name:"scenarioplayer",
			port:8001,
			postmanTag: true
		},
		{
			name:"iointerface",
			port:7000,
			postmanTag: true
		},
		{
			name:"webserver",
			port:6000,
			postmanTag: true
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
	var postmanAddr = addressElements.shift();
	var oscpath = addressElements.join('/');
	
	var postmanElements = postmanAddr.split(':');
	var from = postmanElements.shift();
	var to = postmanElements.shift();
	
	var k = 0;
	for(var k = 0; k<this.services.length; k++){
			if(this.services[k].name == to)
			{
				if (!this.services[k].postmanTag) message[0] = '/'+oscpath;
				return this.services[k].client.sendMessage(message);
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
