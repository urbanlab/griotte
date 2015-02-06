//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#jgs9cx
Blockly.Blocks['settimeout'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(180);
    this.appendDummyInput()
        .appendField("Fais dans");
    this.appendValueInput("time")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("millisecondes");
    this.appendStatementInput("callback");
    this.appendDummyInput()
        .appendField(new Blockly.FieldVariable("handler"), "handler");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('handler')];
  },
  /**
   * Notification that a variable is renaming.
   * If the name matches one of this block's variables, rename it.
   * @param {string} oldName Previous name of variable.
   * @param {string} newName Renamed variable.
   * @this Blockly.Block
   */
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('handler'))) {
      this.setFieldValue(newName, 'handler');
    }
  }
};

//https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#v4jsh2
Blockly.Blocks['cleartimeout'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(195);
    this.appendDummyInput()
        .appendField("Annule")
        .appendField(new Blockly.FieldVariable("handler"), "handler");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('handler')];
  },
  /**
   * Notification that a variable is renaming.
   * If the name matches one of this block's variables, rename it.
   * @param {string} oldName Previous name of variable.
   * @param {string} newName Renamed variable.
   * @this Blockly.Block
   */
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('handler'))) {
      this.setFieldValue(newName, 'handler');
    }
  }
};

Blockly.Blocks['setinterval'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(240);
    this.appendDummyInput()
        .appendField("Fais toutes les");
    this.appendValueInput("time")
        .setCheck("Number");
    this.appendDummyInput()
        .appendField("millisecondes");
    this.appendStatementInput("callback");
    this.appendDummyInput()
        .appendField(new Blockly.FieldVariable("handler"), "handler");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('handler')];
  },
  /**
   * Notification that a variable is renaming.
   * If the name matches one of this block's variables, rename it.
   * @param {string} oldName Previous name of variable.
   * @param {string} newName Renamed variable.
   * @this Blockly.Block
   */
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('handler'))) {
      this.setFieldValue(newName, 'handler');
    }
  }
};

Blockly.Blocks['clearinterval'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(255);
    this.appendDummyInput()
        .appendField("Arrête")
        .appendField(new Blockly.FieldVariable("handler"), "handler");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  },
  getVars: function() {
    return [this.getFieldValue('handler')];
  },
  /**
   * Notification that a variable is renaming.
   * If the name matches one of this block's variables, rename it.
   * @param {string} oldName Previous name of variable.
   * @param {string} newName Renamed variable.
   * @this Blockly.Block
   */
  renameVar: function(oldName, newName) {
    if (Blockly.Names.equals(oldName, this.getFieldValue('handler'))) {
      this.setFieldValue(newName, 'handler');
    }
  }
};
