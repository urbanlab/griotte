function ScenarioListController(element){
		this.currentScenarioList = [];
		this.selectedScenario = {
			name :"",
			path :"",
			element:null
		}
		this.listElement = element; // actually jquery obj more than dom element
}

ScenarioListController.prototype.selectScenario = function(scenarioIndex){
	
	if(this.currentScenarioList.length === 0)
		return;
	
	if(scenarioIndex == -1)
		return this.selectedScenario = {
			name :"",
			path :"",
			element:null
		};
	
	this.selectedScenario = this.currentScenarioList[scenarioIndex];		
}


ScenarioListController.prototype.populateScenarioList = function(list){
	
	this.currentScenarioList = [];
	this.listElement.find(".divider").nextAll().remove();
	
	var self = this;
	list.forEach(function(file){
		self.listElement.append('<li class="scenario-dd-element"><a  href="#"><span class="glyphicon glyphicon-th-list"></span>'+file.filename+'</a></li>');
		var scenario = {
				name :file.filename,
				path :file.filepath,
				element:self.listElement.find("li:last").get(0)
		}
		self.currentScenarioList.push(scenario);

	});
	
	this.listElement.find(".divider").nextAll().uniqueId();
	
}

ScenarioListController.prototype.getScenarioIndexFromElement = function(element){
	var k = 0;
	while(k<this.currentScenarioList.length && this.currentScenarioList[k].element != element)
		k++;
	if(k<this.currentScenarioList.length)
		return k;
	else
		return null;
}

ScenarioListController.prototype.getScenarioIndexFromPath = function(path){
	var k = 0;
	while(k<this.currentScenarioList.length && this.currentScenarioList[k].path != path)
		k++;
	if(k<this.currentScenarioList.length)
		return k;
	else
		return null;	
}
