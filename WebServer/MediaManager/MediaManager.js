var fs = require('fs'),
	path = require('path'),
	Prompt = require('prompt-improved'),
	progress = require('progress-stream');
	
var DEFAULT_MEDIA_DIR = path.join(__dirname, '../media');
var DEFAULT_USB_DIR = '/media/usb';

var SUPPORTED_MEDIA_TYPES = {IMG:"img",VID:"vid",SND:"snd"};
var SUPPORTED_MEDIA_EXT = [{
															type:SUPPORTED_MEDIA_TYPES.IMG,
															list:[".jpeg",".jpg",".JPEG",".JPG"]
														},{
															type:SUPPORTED_MEDIA_TYPES.VID,
															list:[".mov",".avi",".mp4",".mkv",".MOV",".AVI",".MP4",".MKV"]
														},{
															type:SUPPORTED_MEDIA_TYPES.SND,
															list:[".mp3",".MP3",".wav",".WAV"]
														}];



function MediaManager(config){
	if(typeof config === 'undefined')
		return console.log("no config found for MediaManager");
	
	this.mediaDirectory = typeof config.mediaDir !== 'undefined' ? path.resolve(__dirname,"../",config.mediaDir) : DEFAULT_MEDIA_DIR;
	this.USBDirectory = typeof config.USBDir !== 'undefined' ? config.USBDir : DEFAULT_USB_DIR;
	this.pendingTransfer = 0;
	this.mediaList = [];
	//this.updateMediaList();
}

MediaManager.prototype.updateMediaList = function(callback){
	var self = this;
	this.listMedia(this.mediaDirectory,function(err,data){
			if(err)
				return callback(err);
				
			self.mediaList = data;
			return callback(null,self.mediaList);
	});//temporary	
}

// list every media of a directory 
MediaManager.prototype.listMedia = function(dir,callback){
	fs.readdir(dir,function(err,list){
		if(err)
			return callback(err);
		
		var retList = new Array();
		for(var k = 0;k<list.length;k++){
			var ext = path.extname(list[k]);
			for(var i=0;i<SUPPORTED_MEDIA_EXT.length;i++){
				for(var l=0;l<SUPPORTED_MEDIA_EXT[i].list.length;l++){
					if(ext === SUPPORTED_MEDIA_EXT[i].list[l]){
						//temporary
						retList.push({filename:list[k],filepath:path.join(dir,list[k]),filetype:SUPPORTED_MEDIA_EXT[i].type,filesize:fs.statSync(path.join(dir,list[k]))["size"]});
					}
				}
			}
		}
		return callback(null,retList);
		
				
	});
}
// list every media of a directory recursively 
MediaManager.prototype.listMediaRecursive = function(dir,callback)
{
	var self = this;
	var retList = [];
	fs.readdir(dir, function(err, list)
	{
		if (err) 
			return callback(err);
		
		var pending = list.length;
		if (!pending) return callback(null, retList);
		
		list.forEach(function(file)
		{
				
			file = path.resolve(dir, file);
			
			fs.stat(file, function(err, stat) 
			{
					if (stat && stat.isDirectory()) 
					{
						self.listMediaRecursive(file, function(err, res) {
								retList = retList.concat(res);
								if (!--pending) callback(null, retList);
						});
					}
					else
					{
						var ext = path.extname(file);
						for(var i=0;i<SUPPORTED_MEDIA_EXT.length;i++){
							for(var k=0;k<SUPPORTED_MEDIA_EXT[i].list.length;k++)
							{
								if(ext === SUPPORTED_MEDIA_EXT[i].list[k]){
									retList.push({filename:path.basename(file),filepath:file,filetype:SUPPORTED_MEDIA_EXT[i].type,filesize:stat["size"]});
									//retList.push(file);
								}
							}
						}
						if (!--pending) callback(null, retList);
					}
			});
		});
  	});
}

MediaManager.prototype.copyMedia = function(media,from,to,callback){
	
	if(!fs.existsSync(from))
		return callback("Source directory not found ".yellow+from);
	if(!fs.existsSync(to))
		return callback("Destination directory not found ".yellow+to);
	if(!fs.existsSync(path.join(from,media)))
		return callback("Source file missing ".yellow+media);//callback(media+" doesn't exists in "+from);
	if(fs.existsSync(path.join(to,media)))
		return callback('Destination file already exists '.yellow+media);//callback(media+' already exists in '+to);

	console.log(('Copying '+media).yellow);
	
	var is = fs.createReadStream(path.join(from,media));
    var os = fs.createWriteStream(path.join(to,media));
	
    var inStream = fs.createReadStream(path.join(from,media));
    var outStream = fs.createWriteStream(path.join(to,media));
    
    inStream.on('open', function () {
    		
			var stat = fs.statSync(path.join(from,media));
			var str = progress({
				length: stat.size,
				time: 100
			});
			
			str.on('progress', function(progress) {
					process.stdout.clearLine();  // clear current text
					process.stdout.cursorTo(0);
					process.stdout.write(progress.transferred+" / "+progress.length+" ("+progress.percentage+" %) transferred");
			});
			
    		inStream.pipe(str).pipe(outStream);
    		inStream.on('end',function(){
    			return callback(null,'\n'+path.join(from,media)+'\n copied to \n'+path.join(to,media));		
    		});
    		//outStream.end();
    		
    });

    inStream.on('error', function(err) {
    	return callback(err);
    });
    
    outStream.on('error', function(err) {
    	return callback(err);
    });
	
}
MediaManager.prototype.deleteMedia = function(media,callback){
	
}
MediaManager.prototype.renameMedia = function(media,name,callback){
	
}
MediaManager.prototype.loadFromUSBStorage = function(callback)
{
	var self = this;
	
	if(!fs.existsSync(this.USBDirectory)) return callback("USB directory not found ".yellow+this.USBDirectory);
	if(fs.readdirSync(this.USBDirectory).length == 0) return callback("USB drive empty or not mounted ".yellow+this.USBDirectory);
	
	this.listMediaRecursive(this.USBDirectory,function(err,list)
	{
		if(err) return callback(err.red);
		
		var prompt = new Prompt({
			prefix		  : '\n[Media Manager] ',
    		prefixTheme	  : Prompt.chalk.green,
    		textTheme     : Prompt.chalk.bold,
    		timeout       : 10000,
    		attempts	  : 1,
    		inputError    : null,
    		attemptsError : '[Media Manager] Timeout'
		});
		
		prompt.ask(
			[{
				question: "Copy "+list.length+" media from USB storage ? (y|n)\n",
				default: 'N',
				boolean: true,
				key: 'copy'
			}], 
			function(err, res) 
			{
				if (!err && res.copy)
				{
					self.pendingTransfer = list.length; 
					list.forEach(function(element)
					{
						self.copyMedia(element.filename,path.dirname(element.filepath),self.mediaDirectory,function(err,message)
						{		
							if (err) console.log(err.red);
							else console.log('[Media Manager] '.green+message);
							self.pendingTransfer--;
							if (self.pendingTransfer == 0) callback('[Media Manager] '.green+'USB transfer completed');	
						});
					});				
				}
				else return callback('[Media Manager] '.red+'USB transfer canceled');
			}	
		);
		
		
	});
}

module.exports = MediaManager;
