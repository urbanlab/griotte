'use strict';

goog.provide('Blockly.Blocks.video');

goog.require('Blockly.Blocks');
goog.require('Blockly.Medias');

Blockly.Blocks['video_play'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(44);
    this.appendDummyInput()
        .appendTitle("Jouer la vidéo")
        .appendTitle(new Blockly.FieldDropdown(Blockly.Medias.getMediasFor('video')), "VIDEO");
    this.appendDummyInput()
    .appendTitle(new Blockly.FieldDropdown([
                 ["et attendre la fin", "True"],
                 ["et passer à la suite", "False"]]), "SYNC");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Joue la vidéo sélectionnée une seule fois');
  }
};

Blockly.Blocks['video_stop'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(44);
    this.appendDummyInput()
        .appendTitle("Arreter la vidéo en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Couper la vidéo en cours de diffusion');
  }
};


