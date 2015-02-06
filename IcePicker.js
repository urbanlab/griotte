var events = require('events');


function IcePicker(config){
	
	if(typeof config === 'undefined')
		return console.log("no config found for IcePicker");
	
	this.stepsBeforeRampage = typeof config.stepsBeforeRampage !== 'undefined' ? config.stepsBeforeRampage : 10;
	this.timeBetweenSteps = typeof config.timeBetweenSteps !== 'undefined' ? config.timeBetweenSteps : 1000;
	
	this.eventEmitter = new events.EventEmitter();
	this.currentStep = this.stepsBeforeRampage;
	
}

IcePicker.prototype.start = function(){
	var self = this;
	this.walkId = setInterval(function(){
		self.walk();		
	},this.timeBetweenSteps)
}

IcePicker.prototype.stop = function(){
	clearInterval(this.walkId)
	this.currentStep = this.stepsBeforeRampage;
}
IcePicker.prototype.walk = function(){
	this.currentStep--;
	//console.log("IcePicker is walking step = "+this.currentStep);
	if(this.currentStep==0){
		this.eventEmitter.emit('rampage');
		this.stop(); 
	}
}
IcePicker.prototype.pushBack = function(){
	this.currentStep = this.stepsBeforeRampage; 	
}


module.exports = IcePicker;