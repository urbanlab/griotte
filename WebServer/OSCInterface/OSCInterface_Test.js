
// load the OSCInterface module
var OSCInterface = require('./OSCInterface.js');

//'instanciate' the interface
var player = OSCInterface();

// call the interface functions
player.play('hello song');
player.stop();
player.pause();
player.resume();
player.volume(5);
player.mute();
player.unmute();
player.gaussianBlur(2.5);

//process.exit(0);
