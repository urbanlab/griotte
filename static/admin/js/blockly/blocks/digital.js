'use strict';

goog.provide('Blockly.Blocks.digital');
goog.require('Blockly.Blocks');

Blockly.Blocks['digital_sensor'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(349);
    this.appendDummyInput()
        .appendTitle("Capteur Digital");
    this.appendDummyInput()
        .appendTitle("Canal")
        .appendTitle(new Blockly.FieldDropdown([["IO0", "IO0"], ["IO1", "IO1"], ["IO2", "IO2"], ["IO3", "IO3"]]), "CHANNEL");
    this.appendDummyInput()
        .appendTitle("Profil")
        .appendTitle(new Blockly.FieldDropdown([["Bouton", "BUTTON"], ["Grove PIR", "SEN32357P"]]), "PROFILE");
    this.setOutput(true);
    this.setTooltip('');
  }
};

Blockly.Blocks['digital_sensor_edge'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(349);
    this.appendDummyInput()
        .appendTitle("Front")
        .appendTitle(new Blockly.FieldDropdown([["montant", "RISING"], ["descendant", "FALLING"], ["quelconque", "ANY"]]), "EDGE");
    this.appendDummyInput()
        .appendTitle("sur le canal")
        .appendTitle(new Blockly.FieldDropdown([["IO0", "IO0"], ["IO1", "IO1"], ["IO2", "IO2"], ["IO3", "IO3"]]), "CHANNEL");
    this.setOutput(true);
    this.setTooltip('');
  }
};
