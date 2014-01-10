'use strict';

goog.provide('Blockly.Blocks.multimedia');

goog.require('Blockly.Blocks');

Blockly.Blocks['multimedia_audio_play'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Jouer le son")
        // .appendTitle(new Blockly.FieldDropdown([
        //              ["il_fait_chaud.ogg", "il_fait_chaud.ogg"],
        //              ["il_fait_froid.ogg", "il_fait_froid.ogg"],
        //              ["il_fait_bon.ogg", "il_fait_bon.ogg"]]), "audio_play");
        .appendTitle(new Blockly.FieldDropdown([["none","none"]]), "MEDIA");
    this.appendDummyInput()
        .appendTitle(new Blockly.FieldDropdown([
             ["et attendre la fin", "SYNC"],
             ["et passer à la suite", "ASYNC"]]), "METHOD");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Joue le son sélectionné une seule fois');
  },
};

Blockly.Blocks['multimedia_video_play'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Jouer la vidéo")
        .appendTitle(new Blockly.FieldDropdown([
                     ["il_fait_chaud.ogv", "il_fait_chaud.ogv"],
                     ["il_fait_froid.ogv", "il_fait_froid.ogv"],
                     ["il_fait_bon.ogv", "il_fait_bon.ogv"]]), "MEDIA");
    this.appendDummyInput()
    .appendTitle(new Blockly.FieldDropdown([
                 ["et attendre la fin", "SYNC"],
                 ["et passer à la suite", "ASYNC"]]), "METHOD");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Joue la vidéo sélectionnée une seule fois');
  }
};

Blockly.Blocks['multimedia_image_play'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Afficher l'image")
        .appendTitle(new Blockly.FieldDropdown([
                     ["il_fait_chaud.png", "il_fait_chaud.png"],
                     ["il_fait_froid.png", "il_fait_froid.png"],
                     ["il_fait_bon.png", "il_fait_bon.png"]]), "IMAGE");
    this.appendValueInput("DURATION")
        .setCheck("")
        .appendTitle("pendant");
    this.appendDummyInput()
        .appendTitle("secondes");
    this.setInputsInline(true);
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Affiche l\'image sélectionnée pendant le nombre de secondes voulu');
  }
};

Blockly.Blocks['multimedia_volume'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
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

Blockly.Blocks['multimedia_video_stop'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Arreter la vidéo en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Couper la vidéo en cours de diffusion');
  }
};

Blockly.Blocks['multimedia_audio_stop'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Arreter le son en cours");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Couper le son en cours de diffusion');
  }
};

Blockly.Blocks['multimedia_black'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Afficher un écran noir");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip('Afficher un écran noir');
  }
};

Blockly.Blocks['multimedia_wait'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
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
