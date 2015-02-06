var MediaManager 	= require('./MediaManager.js');


mediaManager = new 	MediaManager({"mediaDir": "../media",	"USBDir":"/media/usb"	});
mediaManager.updateMediaList(function(err,data){
	console.log("err  "+err+"  data  "+JSON.stringify(data));	
});

mediaManager.listMediaRecursive("../../media",function(err,data){
	console.log("err  "+err+"  data  "+JSON.stringify(data));		
});