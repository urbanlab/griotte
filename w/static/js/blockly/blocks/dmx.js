
Blockly.Blocks['dmx_send_single'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(120);
    this.appendValueInput("VALUE")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Envoyer immediatement la valeur");
    this.appendValueInput("CHANNEL")
        .setCheck("Number")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("sur le canal DMX");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};

Blockly.Blocks['dmx_send_channels'] = {
  init: function() {
    this.setHelpUrl('http://griotte.erasme.org/');
    this.setColour(140);
    this.appendValueInput("VALUES")
        .setCheck("Array")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("Envoyer les valeurs");
    this.appendValueInput("CHANNELS")
        .setCheck("Array")
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("sur les canaux DMX respectifs");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};

Blockly.Blocks['dmx_blackout'] = {
  init: function() {
    this.setHelpUrl('http://griotte.erasme.org/');
    this.setColour(160);
    this.appendDummyInput()
        .appendField("Eteindre toutes les lumières");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};
