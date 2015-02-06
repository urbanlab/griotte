var fs = require('fs');

var CONFIG_FILE = __dirname +"/globalconfig.json";

exports.loadConfig = function(){
	var configJSON = fs.readFileSync(CONFIG_FILE);
	return JSON.parse(configJSON);
}
exports.savePlayerState = function(){}
	