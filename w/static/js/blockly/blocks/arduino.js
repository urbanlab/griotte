Blockly.Blocks['fonanalog'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(130);
    this.appendDummyInput()
        .appendField("Ecoute");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["A0", "0"], ["A1", "1"], ["A2", "2"], ["A3", "3"], ["A4", "4"], ["A5", "5"]]), "pin");
    this.appendDummyInput()
        .appendField("dans variable :")
        .appendField(new Blockly.FieldVariable("v"), "VAR");  
    this.appendStatementInput("callback");
    this.setInputsInline(true);
    this.setPreviousStatement(false);
    this.setNextStatement(false);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('VAR')];
  },
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('VAR'))) {
      this.setFieldValue(newName, 'VAR');
    }
  }
};


Blockly.Blocks['fwritedigital'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(40);
    this.appendDummyInput()
        .appendField("Ecris")
        .appendField(new Blockly.FieldDropdown([["1", "1"], ["0", "0"]]), "valeur")
        .appendField("sur")
        .appendField(new Blockly.FieldDropdown([["D2", "2"], ["D3", "3"], ["D4", "4"], ["D5", "5"], ["D6", "6"], ["D7", "7"], ["D8", "8"], ["D9", "9"], ["D10", "10"], ["D11", "11"], ["D12", "12"], ["D13", "13"]]), "pin");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};

Blockly.Blocks['fondigitalchange'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(60);
    this.appendDummyInput()
        .appendField("Ecoute Changement");
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown([["D2", "2"], ["D3", "3"], ["D4", "4"], ["D5", "5"], ["D6", "6"], ["D7", "7"], ["D8", "8"], ["D9", "9"], ["D10", "10"], ["D11", "11"], ["D12", "12"], ["D13", "13"]]), "pin");
    this.appendDummyInput()
        .appendField("dans variable :")
        .appendField(new Blockly.FieldVariable("v"), "VAR");   
    this.appendStatementInput("callback");
    this.setInputsInline(true);
    this.setPreviousStatement(false);
    this.setNextStatement(false);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('VAR')];
  },
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('VAR'))) {
      this.setFieldValue(newName, 'VAR');
    }
  }
};

Blockly.Blocks['fwriteservo'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(80);
    this.appendDummyInput()
        .appendField("Place le servo sur")
        .appendField(new Blockly.FieldDropdown([["D3", "3"], ["D5", "5"], ["D6", "6"], ["D9", "9"], ["D10", "10"], ["D11", "11"]]), "pin")
        .appendField("à");
    this.appendValueInput("angle")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("degrès");
    this.setPreviousStatement(true);
    this.setInputsInline(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};

Blockly.Blocks['fwritepwm'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(100);
    this.appendDummyInput()
        .appendField("Ecris");
    this.appendValueInput("valeur")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("sur")
        .appendField(new Blockly.FieldDropdown([["D3", "3"], ["D5", "5"], ["D6", "6"], ["D9", "9"], ["D10", "10"], ["D11", "11"]]), "pin");
    this.setPreviousStatement(true);
    this.setInputsInline(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};