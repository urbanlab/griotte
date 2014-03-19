'use strict';

goog.provide('Blockly.Blocks.analog');

goog.require('Blockly.Blocks');

Blockly.Blocks['analog_sensor'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(349);
    this.appendDummyInput()
        .appendTitle("Capteur Analogique");
    this.appendDummyInput()
        .appendTitle("Canal")
        .appendTitle(new Blockly.FieldDropdown([["AN0", "an0"], ["AN1", "an1"], ["AN2", "an2"], ["AN3", "an3"]]), "CHANNEL");
    this.appendDummyInput()
        .appendTitle("Profil")
        .appendTitle(new Blockly.FieldDropdown([["Identity", "IDENTITY"], ["Maxbotik EZ1", "MAXEZ1"], ["Grove Temperature", "SEN23292P"]]), "PROFILE");
    this.setOutput(true);
    this.setTooltip('');
  }
};
