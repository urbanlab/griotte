function MediaPlayerController(socket,element,mediaListElement){
	this.currentPlayerStatus = {
			isPlaying : false,
			media : null,
			isPaused : false,
			idStoped : false,
			isMuted : false,
			volume : 0,
			zoom : 0,
			blur: 0
	}
	this.element = element // more jQuery object than dom element
	
	this.mediaList = new MediaListController(mediaListElement);
	
	this.socket = socket;
	
	this.addEventListeners();
}

MediaPlayerController.prototype.addEventListeners = function(){
	
	var self = this;
	this.element.find('#play-btn').click(function () {
		if(!self.currentPlayerStatus.isPlaying && self.mediaList.selectedMedia.element !== null)
			self.socket.emit('play',self.mediaList.selectedMedia.path);
	});
	this.element.find('#prev-btn').click(function () {
		self.mediaList.selectPrev();
		if(self.currentPlayerStatus.isPlaying)
			self.socket.emit('play',self.mediaList.selectedMedia.path);
	});
	this.element.find('#next-btn').click(function () {
		self.mediaList.selectNext();
		if(self.currentPlayerStatus.isPlaying)
			self.socket.emit('play',self.mediaList.selectedMedia.path);			
	});
	this.element.find('#pause-btn').click(function () {
		if(!self.currentPlayerStatus.isPaused)
			self.socket.emit('pause');
		else
			self.socket.emit('resume');
			
	});
	this.element.find('#stop-btn').click(function () {
		if(!self.currentPlayerStatus.isStoped)
			self.socket.emit('stop');
	});
	this.element.find('#mute-btn').click(function () {
		if(self.currentPlayerStatus.isMuted)
			self.socket.emit('unmute');
		else
			self.socket.emit('mute');
	});
	this.element.find('#loop-btn').click(function () {
		if(self.currentPlayerStatus.loop)
			self.socket.emit('unloop');
		else
			self.socket.emit('loop');
	});
	this.element.find('#quit-btn').click(function () {
			self.socket.emit('quit');
	});
	this.element.find("#volume-sli").on( "slide", function( event, ui ) {
		self.socket.emit('volume',ui.value);
	});
/*	$("#zoom_sli").on( "slide", function( event, ui ) {
		socket.emit('zoom',ui.value);
	});
	$("#blur_sli").on( "slide", function( event, ui ) {
		socket.emit('blur',ui.value);
	});*/
	$("#media-player").on('click','.media-element',function (event) {
		if(self.currentPlayerStatus.isPlaying){
			self.socket.emit('play',self.mediaList.currentMediaList[self.mediaList.mediaIndex({name:"",path:"",element:event.currentTarget})].path);
		}else{
			self.mediaList.selectMedia(self.mediaList.currentMediaList[self.mediaList.mediaIndex({name:"",path:"",element:event.currentTarget})]);
		}
	});
	
}

MediaPlayerController.prototype.updateMediaList = function(list){
	if( typeof list === 'undefined')
		return;
	
	this.mediaList.populateMediaList(list);
}


MediaPlayerController.prototype.updateWithPlayerStatus = function(status){
		
	if(status.isPlaying){
		var statusMedia = this.mediaList.currentMediaList[this.mediaList.mediaIndexFromPath(status.media.filepath)];
	
		if(!this.currentPlayerStatus.isPlaying ){
			this.element.find('#play-btn').removeClass("btn-default");
			this.element.find('#play-btn').addClass("btn-warning");
			
			this.element.find('#pause-btn').removeClass("disabled");
			
			if(this.mediaList.selectedMedia !== statusMedia)//CCC
				this.mediaList.selectMedia(statusMedia);//CCC

			//CCC
			//$(selectedMedia.element).append('<div id="play-info"><div class="progress" ><div class="progress-bar" style="width:'+100*status.media.progress/status.media.duration+'%;"></div></div></div>');

			
		}else{
			if(this.mediaList.selectedMedia !== statusMedia){
				//this.element.find("#play-info").remove();
				this.mediaList.selectMedia(statusMedia);//CCC
				//CCC
				//$(selectedMedia.element).append('<div id="play-info"><div class="progress" ><div class="progress-bar" style="width:'+100*status.media.progress/status.media.duration+'%;"></div></div></div>');
			}else{
				// update progress
				//console.log("progress  "+100*status.media.progress/status.media.duration);
				this.element.find(".progress-bar").css('width',100*status.media.progress/status.media.duration+'%');
			}
		}
		
	}else{
		if(this.currentPlayerStatus.isPlaying){
			this.element.find('#play-btn').addClass("btn-default");
			this.element.find('#play-btn').removeClass("btn-warning");
			
			this.element.find('#pause-btn').addClass("disabled");
			
			//remove things
			//this.element.find("#play-info").remove();
		}
	}
	if(status.isPaused){
		if(!this.currentPlayerStatus.isPaused){
			this.element.find('#pause-btn').removeClass("btn-default");
			this.element.find('#pause-btn').addClass("btn-warning");
		}
	}else{
		if(this.currentPlayerStatus.isPaused){
			this.element.find('#pause-btn').addClass("btn-default");
			this.element.find('#pause-btn').removeClass("btn-warning");
		}			
	}
	if(status.isMuted){
		if(!this.currentPlayerStatus.isMuted){
			this.element.find('#mute-btn').removeClass("btn-default");
			this.element.find('#mute-btn').addClass("btn-warning");
		}
	}else{
		if(this.currentPlayerStatus.isMuted){
			this.element.find('#mute-btn').addClass("btn-default");
			this.element.find('#mute-btn').removeClass("btn-warning");
		}
	}
	if(status.loop){
		if(!this.currentPlayerStatus.loop){
			this.element.find('#loop-btn').removeClass("btn-default");
			this.element.find('#loop-btn').addClass("btn-warning");
		}
	}else{
		if(this.currentPlayerStatus.loop){
			this.element.find('#loop-btn').addClass("btn-default");
			this.element.find('#loop-btn').removeClass("btn-warning");
		}
	}
	if(status.volume !== this.currentPlayerStatus.volume){
		this.element.find("#volume-sli").slider("value",status.volume);
	}
	/*console.log(status.zoom);
	if(status.zoom !== currentPlayerStatus.zoom){
		$("#zoom_sli").slider("value",status.zoom);
	}
	if(status.blur !== currentPlayerStatus.blur){
		$("#blur_sli").slider("value",status.blur);
	}*/
	
	this.currentPlayerStatus = status;
}
