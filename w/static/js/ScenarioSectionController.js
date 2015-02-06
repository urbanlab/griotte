function ScenarioSectionController(socket,element,scenarioListElement){
	
	this.element = element // more jQuery object than dom element
	
	this.scenarioList = new ScenarioListController(scenarioListElement);
	
	this.socket = socket;
	
	this.currentScenario = {
		name:"scenario",
		type:"block",
		xml:"",
		coejs:"",
		codepy:""
	};
	
	this.addEventListeners();
}

ScenarioSectionController.prototype.addEventListeners = function(){
	
	var self = this;
	this.element.find('#add-scenario-btn').click(function () {
	});
	this.element.find('#create-scenario-btn').click(function () {
			var name = $("#new-sco-ti").val();
			var type = $(".select-sco-type #sco-type-block-btn").hasClass("selected") ? "block" : "script";
			
			self.createScenario(name,type);
	});
	this.element.find('#play-scenario-btn').click(function () {
			self.playScenario();
	});
	this.element.find('#stop-scenario-btn').click(function () {
			self.stopScenario();
	});
	this.element.find('#save-scenario-btn').click(function () {
			$(this).addClass("btn-warning");
			self.saveScenario();
	});
	this.element.find('#delete-scenario-btn').click(function () {
	});
	this.element.find('#delete-sco-confirm-btn').click(function () {
			self.deleteScenario();
	});
	this.element.find('#upload-scenario-btn').click(function () {
	});
	this.element.find('#download-scenario-btn').click(function () {
	});
	$("#scenario-section").on('click','.scenario-dd-element',function (event) {
		self.selectScenario(self.scenarioList.getScenarioIndexFromElement(event.currentTarget));

	});
}

ScenarioSectionController.prototype.selectScenario = function(scenarioIndex){
	this.scenarioList.selectScenario(scenarioIndex);
	this.socket.emit('getScenario',this.scenarioList.selectedScenario.path);
}

ScenarioSectionController.prototype.resetSelection = function(){
	
	this.scenarioList.selectScenario(-1);
	this.updateCurrentScenario({
		name:"scenario",
		type:"block",
		xml:"",
		coejs:"",
		codepy:""
	});
}

ScenarioSectionController.prototype.updateMediaList = function(list){
	Blockly.Medias.populateMediaList(list);
}

ScenarioSectionController.prototype.updateScenarioList = function(list){
	
	if( typeof list === 'undefined')
		return;
	
	this.scenarioList.populateScenarioList(list);
}

ScenarioSectionController.prototype.updateCurrentScenario = function(scenario){
	this.currentScenario = scenario;
	this.element.find("#scenario-dd-btn #current-sco-label").text(this.currentScenario.name);
	if(this.currentScenario.type == "block")
		this.updateBlockly();
}

ScenarioSectionController.prototype.updateBlockly = function(){
	
	if (Blockly.mainWorkspace !== null)
		Blockly.mainWorkspace.clear();
	
  var xml = Blockly.Xml.textToDom("<xml>"+this.currentScenario.xml+"</xml>")
  Blockly.Xml.domToWorkspace(Blockly.getMainWorkspace(), xml);
}

ScenarioSectionController.prototype.createScenario = function(name,type){
	var scenario = {
		name:name,
		type:type,
		xml:"",
		codejs:"",
		codepy:""
	}
	this.socket.emit('createScenario',scenario);
}

ScenarioSectionController.prototype.playScenario = function(){
	this.socket.emit("playScenario",this.currentScenario.name,Blockly.JavaScript.workspaceToCode());
	//this.socket.emit("playScenario",this.currentScenario.name,this.currentScenario.codejs);
}
ScenarioSectionController.prototype.stopScenario = function(){
	this.socket.emit("stopScenario");
}
ScenarioSectionController.prototype.saveScenario = function(){
 
	//if (!Code.current_scenario || (Code.current_scenario.length == 0)) {
  //  return;
  //}

  this.currentScenario.xml = Blockly.Xml.workspaceToDom(Blockly.getMainWorkspace()).innerHTML;
  //this.currentScenario.codepy = this.wrapPyScenario(Blockly.Python.workspaceToCode());
  this.currentScenario.codejs = Blockly.JavaScript.workspaceToCode();
  console.log(this.currentScenario);
  
  this.socket.emit('saveScenario',{scenariopath:this.scenarioList.selectedScenario.path,scenario:this.currentScenario});
}
// temporary
ScenarioSectionController.prototype.wrapPyScenario = function(code) {
  var lines = code.split('\n');

  code = "def run():";
  code += "\n";

  for(var i = 0; i < lines.length; i++) {
    code += "  " + lines[i] + "\n";
  }

  code += "\n";

  var tail = [
    '',
    'if __name__ == "__main__":',
    '  from griotte.config import Config',
    '  Config("DEFAULT")',
    '  run()',
    ].join('\n');

  code = code + tail;
  console.log(code);

  return code;
};

ScenarioSectionController.prototype.deleteScenario = function(){
	this.socket.emit('deleteScenario',this.scenarioList.selectedScenario.path);
}
ScenarioSectionController.prototype.uploadScenario = function(){
	
}
ScenarioSectionController.prototype.downloadScenario = function(){
	
}
