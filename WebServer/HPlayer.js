
/***** HPlayer Model Class ****/

function HPlayer(config){

	this.pid 		= null;
	this.name 		= "Roberto";
	this.ip = "127.0.0.1";
	this.isPlaying 	= false;
	this.media = {
		filepath:	null,
		progress:	null,
		duration:	null
	}
	this.loop		= false;
	this.isPaused 	= false;
	this.isMuted 	= false;
	this.volume 	= 50;
	this.zoom 		= 10;
	this.blur 		= 0;
	this.hdmiAudio	= false;
	this.info		= false;
	
	if (config)
	{ 
		this.status(config);
		this.hdmiAudio	= config.hdmiAudio;
		this.info		= config.info;
		this.ip = config.ip;
	}
}

HPlayer.prototype.status = function(status){
	
	if(typeof status !== 'undefined')
	{
		this.name = status.name;
		this.isPlaying = status.isPlaying;
		this.media = status.media;
		this.isPaused = status.isPaused;
		this.isMuted = status.isMuted;
		this.volume = status.volume;
		this.zoom = status.zoom;
		this.blur = status.blur;
		this.loop = status.loop;
	}

	
	return {
		name : this.name,
		ip : this.ip,
		isPlaying : this.isPlaying,
		media : this.media,
		isPaused : this.isPaused,
		isMuted : this.isMuted,
		volume : this.volume,
		zoom : this.zoom,
		blur : this.blur,
		loop : this.loop,
		hdmiAudio : this.hdmiAudio,
		info : this.info
	}
		
}

module.exports = HPlayer;
