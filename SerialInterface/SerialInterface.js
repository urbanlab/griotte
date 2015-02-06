var sp = require("serialport"),
	events = require('events');

var SerialPort = sp.SerialPort;



/*** Command class ****/

function Command(){
	this.name = "";
	this.args = [];	
}

Command.prototype.parseString = function(string){
	// command  sent as stringified JSON = easy parse ;)
	try {
		var json = JSON.parse(string);
		this.name = json.name;
		this.args = json.args;
		return true;
	}
	catch (e) {
		console.log("parsing error: "+e);
		return false;
	};

}



/*****************  SerialInterface Class *************************************/

function SerialInterface(config){
	
	if(typeof config === 'undefined')
		return console.log("no config found for SerialInterface");
	
	this.baudRate = typeof config.baudRate !== 'undefined' ? config.baudRate : 9600;
	this.DataFormater = typeof config.DataFormater !== 'undefined' ? config.DataFormater : {};
	
	this.eventEmitter = new events.EventEmitter();
	this.arduinoComList = [];
	
}	

SerialInterface.prototype.start = function(){
	var self = this;
	this.getArduinoComList(function(err,list){
			
		if(err)
			return console.log(err);

		console.log(list);
		self.arduinoComList = list;
		
		if(self.arduinoComList.length == 0)
			return console.log("serial error : no arduino com port found");
		if(self.arduinoComList.length>1)
			console.log("more than one arduino device found.. first take first");
		
		self.serialPort = new SerialPort(self.arduinoComList[0], {
				baudrate: this.baudRate,
				parser: sp.parsers.readline("\n")
		},false);		
		
		self.open();
	});
}

SerialInterface.prototype.open = function(){
	this.addEventListeners();
	this.serialPort.open(function(err){if(err)console.log(err)});
}

SerialInterface.prototype.addEventListeners = function(){
	this.serialPort.on('open', this.openHandler.bind(this));
	this.serialPort.on('data',this.dataHandler.bind(this));
	this.serialPort.on('close', this.closeHandler.bind(this));
	this.serialPort.on('error', this.errorHandler.bind(this));
}
SerialInterface.prototype.removeEventListeners = function(){
	this.serialPort.removeEventListener('open', this.openHandler);
	this.serialPort.removeEventListener('data', this.dataHandler);
	this.serialPort.removeEventListener('close', this.closeHandler);
	this.serialPort.removeEventListener('error', this.errorHandler);
}

/** EVENT HANDLERS **/

SerialInterface.prototype.openHandler = function(){
	this.eventEmitter.emit("open");
}
SerialInterface.prototype.closeHandler = function(){
	this.eventEmitter.emit("close");
}
SerialInterface.prototype.errorHandler = function(err){
	this.eventEmitter.emit("error",err);
}
SerialInterface.prototype.dataHandler = function(data){
	command = new Command();
	//command.name = "volume";
	//command.args = {"value":parseInt(data)};
	if(!command.parseString(data))
		return;
	//console.log(JSON.stringify(command));
	switch (command.name){
		case "volume":
			this.eventEmitter.emit("volume",command.args.value);
			break;
		case "gaussianBlur":
			this.eventEmitter.emit("blur",command.args.value);
			break;
		default: console.log("serial command not recognized: "+command.name);		
	}
	
	
}


SerialInterface.prototype.write = function(buffer,callback){
	this.serialPort.write(buffer,callback);	
}

SerialInterface.prototype.close = function(){	
	this.serialPort.open(function(err){if(err)console.log(err)});
	this.removeEventListener();
}

SerialInterface.prototype.getArduinoComList = function(callback){
	var alist = [];
	sp.list(function (err, ports) {
		if(err)
			return callback(err)
			
		for(var k=0;k<ports.length;k++){
			//console.log(JSON.stringify(ports[k]));
			if(ports[k].pnpId.indexOf("Arduino") > -1 || ports[k].manufacturer.indexOf("Arduino") > -1){
				//console.log(ports[k].pnpId.indexOf("Arduino"))
				alist.push(ports[k].comName);
			}
		}
		
		return callback(null,alist);
  	});
}


module.exports = SerialInterface;
