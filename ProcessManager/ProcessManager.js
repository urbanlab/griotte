var process = require('child_process'),
	colors = require('colors');
	
var RESPAWN_DELAY = 1000;


function ProcessManager(){
	this.childProcesses = [];		
}

ProcessManager.prototype.spawn = function(proc,args,autorespawn,pipestdout){
	
	var self = this;
	var child = process.spawn(proc,args);
	
	if(pipestdout){
		child.stdout.setEncoding('utf8');
		child.stdout.on('data', function (data) {
				console.log(data);
		});
	}else
		child.stdout = 'ignore';
	
	child.on('exit', function (code,signal) {
			console.log('[Process Manager] '+this.pid+' exited with code '.red+code+' and signal '.red+signal);
			var i = self.getProcessIndex(this.pid);			
			if(i !== -1){
				self.childProcesses.splice(i,1);
				if(autorespawn){
					console.log("[Process Manager]".yellow+" shoot again !");
					setTimeout(function(){
							self.spawn(proc,args,autorespawn,pipestdout);
					},RESPAWN_DELAY);
				}
			}
	});
	child.on('error', function (err) {
			console.log('[Process Manager] '+this.pid+'  error : '+err);
			var i = self.getProcessIndex(this.pid);			
			if(i !== -1){
				self.childProcesses.splice(i,1);
				if(autorespawn){
					console.log("[Process Manager]".yellow+" shoot again !");
					setTimeout(function(){
							self.spawn(proc,args,autorespawn,pipestdout);
					},RESPAWN_DELAY);
				}
			}
			
			this.kill('SIGTERM');// just in case of zombie attack
	});
	
	this.childProcesses.push(child)
	console.log(('[Process Manager] ').green+proc+' started with pid '+child.pid);	
}

ProcessManager.prototype.killAll = function(){
	for (var i in this.childProcesses) this.kill(this.childProcesses[i].pid);
}

ProcessManager.prototype.kill = function(pid){
	
	var i = this.getProcessIndex(pid);
	if(i == -1) return console.log("[Process Manager]".yellow+" pid doesn't exists");
	
	this.childProcesses[i].kill('SIGKILL');
	this.childProcesses.splice(i,1);
	
	console.log('[Process Manager] '.red+pid+' killed');
}

ProcessManager.prototype.getProcessIndex = function(pid){
	var k=0;
	while(k<this.childProcesses.length && this.childProcesses[k].pid !== pid)
		k++;
	if(k<this.childProcesses.length)
		return k;
	else
		return -1;
}

ProcessManager.prototype.cleanZombies = function(processName) {
	
	var self = this;
	
	process.exec('pgrep '+processName, function (error, stdout, stderr) 
	{
		//if (error) { console.error(error); }
		pids = stdout.split("\n");
		for(var i=0; i<pids.length;i++) pids[i] = +pids[i];
		
		pids.forEach(function( pid )
		{
			if ((pid > 0) && ( self.getProcessIndex(pid) == -1))
				process.exec('kill -9 '+pid, function (error, stdout, stderr) {
					console.log( ('[Process Manager] '+processName+' zombie '+pid+' killed').yellow ); });
		});
	});
}


 module.exports = ProcessManager;
