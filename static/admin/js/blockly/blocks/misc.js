'use strict';

goog.provide('Blockly.Blocks.misc');

goog.require('Blockly.Blocks');
goog.require('Blockly.Medias');

Blockly.Blocks['misc_volume'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(44);
    this.appendValueInput("VOLUME")
        .setCheck("")
        .appendTitle("Régler le son à");
    this.appendDummyInput()
        .appendTitle("%");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Règle le volume du son entre 0% et 120%');
  }
};

Blockly.Blocks['misc_wait'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(44);
    this.appendValueInput("DURATION")
        .setCheck("")
        .appendTitle("Attendre pendant");
    this.appendDummyInput()
        .appendTitle("secondes");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Bloquer le déroulement du scénario pendant un certain temps');
  }
};


