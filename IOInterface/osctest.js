var osc = require('node-osc');

var oscClient = new osc.Client("192.168.0.16", 6001); 
oscClient.sendMessage = function (operation,args){
		var message = new osc.Message('raspiomix/'+operation);
		if(typeof args !== 'undefined')// we got args
			for(var k=0;k<args.length;k++)// we push args
				message.append(args[k]);
	//console.log(JSON.stringify(message)+"  "+args);
	console.log(message);
		this.send(message);	
}
var now;
var oscServer = new osc.Server(6000, "127.0.0.1");

oscServer.on("message", function(message,rinfo){
		var date = new Date();
		console.log(date.getTime() - now);
		console.log(message);
		console.log(rinfo);
});	
	
	
	
setInterval(function(){
		var date = new Date();
		now = date.getTime();
		//console.log(now)
		oscClient.sendMessage("getAnalog",[0,"salut",3.45]);
		
},1000);
