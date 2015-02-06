var path = require('path');
var MediaManager = require('./MediaManager/MediaManager.js');
	
var mediaManager = new MediaManager();

mediaManager.listMediaRecursive('./',function(err,data){
	if(err)
		return console.log(err);
	
	data.forEach(function(media){
			mediaManager.copyMedia(path.basename(media),path.dirname(media),mediaManager.mediaDirectory,function(err,data){
				if(err)
					return console.log(err);
				
				console.log(data);
			});	
	});
});