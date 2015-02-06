'use strict';

goog.provide('Blockly.Blocks.image');

goog.require('Blockly.Blocks');
goog.require('Blockly.Medias');

Blockly.Blocks['image_play'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(44);
    this.appendDummyInput()
        .appendTitle("Afficher l'image")
        .appendTitle(new Blockly.FieldDropdown(Blockly.Medias.getMediasFor('img')), "IMAGE");
    // this.appendValueInput("DURATION")
    //     .setCheck("")
    //     .appendTitle("pendant");
    // this.appendDummyInput()
    //     .appendTitle("secondes");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Affiche l\'image sélectionnée');
  }
};

Blockly.Blocks['image_set_background'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(44);
    this.appendValueInput("COLOR")
        .setCheck("")
        .appendTitle("Afficher un écran");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Afficher un écran de couleur');
  }
};
