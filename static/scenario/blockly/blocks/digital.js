'use strict';

goog.provide('Blockly.Blocks.digital');

goog.require('Blockly.Blocks');

Blockly.Blocks['capteur_digital'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(65);
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
