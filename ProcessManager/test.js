var ProcessManager = require('./ProcessManager.js');
	
	pm = new ProcessManager();
	//pm.spawn('ys',[],true,true);
	pm.spawn('ls',['-la'],true,true);