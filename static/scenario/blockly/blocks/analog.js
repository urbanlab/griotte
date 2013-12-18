'use strict';

goog.provide('Blockly.Blocks.analog');

goog.require('Blockly.Blocks');

Blockly.Blocks['capteur_analogique'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(260);
    this.appendDummyInput()
        .appendTitle("Capteur Analogique");
    this.appendDummyInput()
        .appendTitle("Canal")
        .appendTitle(new Blockly.FieldDropdown([["AN0", "AN0"], ["AN1", "AN1"], ["AN2", "AN2"], ["AN3", "AN3"]]), "NAME");
    this.appendDummyInput()
        .appendTitle("Profil")
        .appendTitle(new Blockly.FieldDropdown([["Identity", "IDENTITY"], ["Maxbotik EZ1", "MAXEZ1"], ["Grove Temperature", "SEN23292P"]]), "Profil");
    this.setOutput(true);
    this.setTooltip('');
  }
};
