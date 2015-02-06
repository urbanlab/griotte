function MediaListController(tableElement){
		this.currentMediaList = [];
		this.selectedMedia = {
			name :"",
			path : "",
			element:null
		}
		this.table = tableElement; // actually jquery obj more than dom element
}

MediaListController.prototype.selectMedia = function(media){
	
	if(this.currentMediaList.length === 0)
		return;

	if(!this.selectedMedia.element){
		$(media.element).addClass("active")
	}else if(media.element.id !== this.selectedMedia.element.id){
		$(media.element).addClass("active");
		$(this.selectedMedia.element).removeClass("active");
	}else{
		return;
	}
	this.selectedMedia = media;		
}

MediaListController.prototype.selectNext = function(){
	var next = $(this.selectedMedia.element).next();
	if(next.get(0) === undefined)
		next = this.table.find("tbody tr").first();
	this.selectMedia(this.currentMediaList[this.mediaIndex({name:"",path:"",element:next.get(0)})]);
}

MediaListController.prototype.selectPrev = function(){
	var prev = $(this.selectedMedia.element).prev();
	if(prev.get(0) === undefined)
		prev = this.table.find("tbody tr").last();
	this.selectMedia(this.currentMediaList[this.mediaIndex({name:"",path:"",element:prev.get(0)})]);
}

MediaListController.prototype.populateMediaList = function(list){
	
	// we do it the hard way for the moment :
	this.currentMediaList = [];
	this.table.find("tbody").empty();
	
	var self = this;
	list.forEach(function(file){
		self.table.find("tbody").append('<tr class="media-element"><td><span class="glyphicon '+self.getIconFromFiletype(file.filetype)+'"></span></td><td>'+file.filename+'</td><td>55:02</td><td>'+filesize(file.filesize)+'</td></tr>');
		var media = {
				name :file.filename,
				path :file.filepath,
				type :file.filetype,
				size :file.filesize,
				element:self.table.find("tbody tr:last").get(0)
		}
		self.currentMediaList.push(media);

	});
	
	this.table.find("tbody").children().uniqueId();
	
	//if(!this.selectedMedia.element && this.currentMediaList.length > 0)
		//selectMedia(this.currentMediaList[0]);
}


MediaListController.prototype.mediaIndex = function(media){
	var k = 0;
	while(k<this.currentMediaList.length && this.currentMediaList[k].element.id != media.element.id)
		k++;
	if(k<this.currentMediaList.length)
		return k;
	else
		return null;
}

MediaListController.prototype.mediaIndexFromPath = function(filepath){
	var k = 0;
	while(k<this.currentMediaList.length && this.currentMediaList[k].path != filepath)
		k++;
	if(k<this.currentMediaList.length)
		return k;
	else
		return null;
}

MediaListController.prototype.getIconFromFiletype = function(filetype){
	
	switch(filetype){
		case "vid" : return "glyphicon-film";
		case "img" : return "glyphicon-picture";
		case "snd" : return "glyphicon-music";
		default : return "glyphicon-file";
	}
}
