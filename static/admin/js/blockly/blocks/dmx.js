'use strict';

goog.provide('Blockly.Blocks.dmx');

goog.require('Blockly.Blocks');

Blockly.Blocks['dmx_send_single'] = {
  init: function() {
    this.setHelpUrl('http://griotte.erasme.org/');
    this.appendDummyInput()
        .appendField("Envoyer la valeur")
        .appendField(new Blockly.FieldTextInput("0"), "VALUE")
        .appendField("sur le canal DMX")
        .appendField(new Blockly.FieldTextInput("1"), "CHANNEL");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('');
  }
};


