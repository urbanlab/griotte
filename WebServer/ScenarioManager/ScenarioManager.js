var fs = require('fs'),
		sanitize = require("sanitize-filename"),
		path = require('path');
	
var DEFAULT_SCENARIO_DIR = path.join(__dirname, './scenario');	
var SCENARIO_FILE_EXT = ".sco"
	
function ScenarioManager(config){

	if(typeof config === 'undefined')
		return console.log("no config found for ScenarioManager");
	
	this.scenarioDirectory = typeof config.scenarioDir !== 'undefined' ? path.resolve(__dirname,"../",config.scenarioDir) : DEFAULT_SCENARIO_DIR;	
	this.scenarioList = [];
}


ScenarioManager.prototype.getScenario = function(path){
		var scoFile = fs.readFileSync(path);
		return JSON.parse(scoFile);
}

ScenarioManager.prototype.updateScenarioList = function(callback){
	var self = this;
	this.listScenario(this.scenarioDirectory,function(err,data){
			if(err)
				return callback(err);
				
			self.scenarioList = data;
			return callback(null,self.scenarioList);
	});//temporary	
}

// list every scenario of a directory recursively 
// TODO : separate example scenarios from user scenarios
ScenarioManager.prototype.listScenario = function(dir,callback)
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
						self.listScenario(file, function(err, res) {
								retList = retList.concat(res);
								if (!--pending) callback(null, retList);
						});
					}
					else
					{
						var ext = path.extname(file);
						if(ext === SCENARIO_FILE_EXT){
							retList.push({filename:path.basename(file),filepath:file});
						}
						if (!--pending) callback(null, retList);
					}
			});
		});
  	});
}

ScenarioManager.prototype.copyScenario = function(scenario,from,to,callback){
	
	/*if(!fs.existsSync(from))
		return callback("Source directory not found ".yellow+from);
	if(!fs.existsSync(to))
		return callback("Destination directory not found ".yellow+to);
	if(!fs.existsSync(path.join(from,scenario)))
		return callback("Source file missing ".yellow+scenario);//callback(scenario+" doesn't exists in "+from);
	if(fs.existsSync(path.join(to,scenario)))
		return callback('Destination file already exists '.yellow+scenario);//callback(scenario+' already exists in '+to);

	console.log(('Copying '+scenario).yellow);
	
	var is = fs.createReadStream(path.join(from,scenario));
    var os = fs.createWriteStream(path.join(to,scenario));
	
    var inStream = fs.createReadStream(path.join(from,scenario));
    var outStream = fs.createWriteStream(path.join(to,scenario));
    
    inStream.on('open', function () {
    		
			var stat = fs.statSync(path.join(from,scenario));
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
    			return callback(null,'\n'+path.join(from,scenario)+'\n copied to \n'+path.join(to,scenario));		
    		});
    		//outStream.end();
    		
    });

    inStream.on('error', function(err) {
    	return callback(err);
    });
    
    outStream.on('error', function(err) {
    	return callback(err);
    });*/
	
}
ScenarioManager.prototype.createScenario = function(scenario,callback){
	var self = this;
	var p = path.join(this.scenarioDirectory,sanitize(scenario.name+".sco"));
	this.saveScenario(p,scenario,function(scenariopath){
			self.updateScenarioList(function(err,list){
					callback(scenariopath,list);
			});
	});
}
// TO BE TESTED
ScenarioManager.prototype.saveScenario = function(scenariopath,scenario,callback){
	
	//if(!fs.existsSync(scenariopath))
		//return console.error("save error : scenario doesn't exist");
	
	fs.writeFile(scenariopath, JSON.stringify(scenario,null,2), function (err) {
		if (err) 
			console.error(err);
		
		callback(scenariopath);
		console.log("scenario saved");
	});
	
	
	
}
ScenarioManager.prototype.deleteScenario = function(scenariopath,callback){
	var self = this;
	fs.unlink(scenariopath, function (err) {
		if (err) 
				console.error(err);
  	
		self.updateScenarioList(function(err,list){
				callback(list);
		});
		console.log("scenario deleted");
  });
}
ScenarioManager.prototype.renameScenario = function(scenario,name,callback){
	
}

module.exports = ScenarioManager;