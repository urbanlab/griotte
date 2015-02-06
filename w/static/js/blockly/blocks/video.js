'use strict';

goog.provide('Blockly.Blocks.video');

goog.require('Blockly.Blocks');
goog.require('Blockly.Medias');

Blockly.Blocks['video_play'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(230);
    this.appendDummyInput()
        .appendTitle("Jouer la vidéo")
        .appendTitle(new Blockly.FieldDropdown(Blockly.Medias.getMediasFor('vid')), "VIDEO");
    this.appendDummyInput("lire en boucle")
        .appendField(new Blockly.FieldCheckbox("TRUE"), "loop_cb")
        .appendField("en boucle");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Joue la vidéo sélectionnée une seule fois');
  }
};
Blockly.Blocks['video_pause'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(260);
    this.appendDummyInput()
        .appendTitle("Mettre en pause la vidéo en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Blocks['video_resume'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(260);
    this.appendDummyInput()
        .appendTitle("Reprendre la vidéo en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
  }
};
Blockly.Blocks['video_stop'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(290);
    this.appendDummyInput()
        .appendTitle("Arreter la vidéo en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Couper la vidéo en cours de diffusion');
  }
};


