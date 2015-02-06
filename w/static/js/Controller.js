

function Controller(){
	
	  this.gui = new GUI();
	
	
	 	if (!window.location.origin)
  			window.location.origin = window.location.protocol+"//"+window.location.host;
		this.socket = io.connect(window.location.origin);
	
		// media list in medias section
		//this.msMediaListController = new MediaListController($("#media-section .medialist"));
		
		//media player
		this.mediaPlayer = new MediaPlayerController(this.socket,$("#media-player #player-controls"),$("#media-player .media-list"));
		
		this.mediaSection = new MediaSectionController(this.socket,$("#media-section"),$("#media-section .media-list"));	

		this.scenarioSection = new ScenarioSectionController(this.socket,$("#scenario-section"),$("#scenario-section #scenario-dd"))
		
		this.addEventListeners();

}

Controller.prototype.addEventListeners = function(){
	
	var self = this;
	this.socket.on('connect', function (data) {
			console.log('connected');
	});
	
	this.socket.on('networkInfo', function (info) {
		console.log(info);
		$('#player-head .player-name').text(info.hostname);
		$('#player-head .player-ip').text(info.ip);
		document.title = info.hostname;
	});	
	
	this.socket.on('playerStatus', function (status) {

		self.mediaPlayer.updateWithPlayerStatus(status);
		console.log(status);
	});
	
	this.socket.on('scenarioPlayerStatus', function (status) {
		var spStatus = JSON.parse(status);
		self.gui.changeSpStatus(spStatus);
		console.log(spStatus);
	});
	
	this.socket.on('mediaList', function (list) {
		self.mediaPlayer.updateMediaList(list);
		self.mediaSection.updateMediaList(list);
		self.scenarioSection.updateMediaList(list);
		//console.log(list);
	});
	
	this.socket.on('scenarioList', function (list) {
		console.log(list);
		self.scenarioSection.updateScenarioList(list);
	});
	this.socket.on('scenario', function (scenario) {
		//console.log(scenario);
		self.scenarioSection.updateCurrentScenario(scenario);
		self.gui.changeScenarioSubState(self.gui.scenarioSubStates.scenarioloaded);
	});
	this.socket.on('scenarioSaved', function (scenariopath) {
		$("#save-scenario-btn").removeClass("btn-warning");
	});
	this.socket.on('scenarioCreated', function (scenariopath,scenarioList) {
		console.log("scenario created  : "+scenariopath);
		self.scenarioSection.updateScenarioList(scenarioList);
		self.scenarioSection.selectScenario(self.scenarioSection.scenarioList.getScenarioIndexFromPath(scenariopath));
		self.gui.closePopup();
	});
	this.socket.on('scenarioDeleted', function (scenarioList){
		self.scenarioSection.updateScenarioList(scenarioList);
		self.scenarioSection.resetSelection();
		self.gui.changeScenarioSubState(self.gui.scenarioSubStates.scenarioempty);
		self.gui.closePopup();
	})
	
}
	
	

