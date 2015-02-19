var firmata = require("firmata");

//analogs = [0, 1, 2, 3, 4, 5];

function FirmataInterface(){
	var self = this;
	var options = {
		samplingInterval:50
	}
	this.board = new firmata.Board("/dev/ttyACM0", options,function(err) {
		if (err) {
			console.log(err);
			return;
  	}
  	console.log("connected");
  	console.log("Firmware: " + self.board.firmware.name + "-" + self.board.firmware.version.major + "." + self.board.firmware.version.minor);
  });
  
}

FirmataInterface.prototype.onAnalog = function(pin,callback){
	//console.log(this.board.pins);
	if(this.board.pins[this.board.analogPins[pin]].mode !== this.board.MODES.ANALOG)
		this.board.pinMode(pin,this.board.MODES.ANALOG);
	
	this.board.analogRead(pin,callback);
	
}

FirmataInterface.prototype.onDigitalChange = function(pin,callback){
	if(this.board.pins[pin].mode !== this.board.MODES.INPUT)
		this.board.pinMode(pin,this.board.MODES.INPUT);
	
	this.board.digitalRead(pin,callback);
}

FirmataInterface.prototype.writeDigital = function(pin,value){
	if(this.board.pins[pin].mode !== this.board.MODES.OUTPUT)
		this.board.pinMode(pin,this.board.MODES.OUTPUT);
	
	this.board.digitalWrite(pin,value);
}

FirmataInterface.prototype.writePWM = function(pin,value){
	if(this.board.pins[pin].mode !== this.board.MODES.PWM)
		this.board.pinMode(pin,this.board.MODES.PWM);
	
	this.board.analogWrite(pin,value);

}

FirmataInterface.prototype.writeServo = function(pin,value){
	if(this.board.pins[pin].mode !== this.board.MODES.SERVO)
		this.board.pinMode(pin,this.board.MODES.SERVO);
	
	this.board.servoWrite(pin,value);
	
}

// quick and dirty
FirmataInterface.prototype.resetAll = function(){
	this.board.removeAllListeners();
}

module.exports = FirmataInterface;