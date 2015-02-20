function MediaSectionController(socket,element,mediaListElement){
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

MediaSectionController.prototype.addEventListeners = function(){
	
	var self = this;
	this.element.find('#add-media-btn').click(function () {
	});
	this.element.find('#download-media-btn').click(function () {
	});
	this.element.find('#delete-media-btn').click(function () {
		if(self.mediaList.selectedMedia.element !== null)
			self.socket.emit('deleteMedia',self.mediaList.selectedMedia.path);
	});
	
	$("#media-section").on('click','.media-element',function (event) {
		self.mediaList.selectMedia(self.mediaList.currentMediaList[self.mediaList.mediaIndex({name:"",path:"",element:event.currentTarget})]);
	});
}

MediaSectionController.prototype.updateMediaList = function(list){
	if( typeof list === 'undefined')
		return;
	
	this.mediaList.populateMediaList(list);
}
