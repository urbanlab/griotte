// check OLA configuration
//http://192.168.x.xx:9090/ola.html


var DMX = require('dmx');


function DMXInterface(){
	
	this.dmx = new DMX();
	//this.universe = this.dmx.addUniverse('myuniverse', 'enttec-usb-dmx-pro', 0);
	this.universe = this.dmx.addUniverse('myuniverse', 'null', 0);
}

DMXInterface.prototype.send = function(channel,value){
	var val = {};
	val[channel] = value
	this.universe.update(val);
	console.log(this.universe);
}

DMXInterface.prototype.sendM = function(valueObj){
	// valueObj : {chan0:val0,chan15:val15,...}
	this.universe.update(valueObj);
	console.log(this.universe);
	
}

DMXInterface.prototype.blackout = function(){
	values = {};
	for(var i=0;i<512;i++)
		values[i] = 0;
	
	//console.log(values);
	this.universe.update(values);
	console.log(this.universe);
}
/*var dmxInterface = new DMXInterface();
dmxInterface.send(3,0xFF);
console.log(dmxInterface.universe);
dmxInterface.sendM({0:0xAA,2:0xBB,4:0xCC});
console.log(dmxInterface.universe);
dmxInterface.blackout();
console.log(dmxInterface.universe);*/

module.exports = DMXInterface;