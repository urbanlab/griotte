'use strict';

goog.provide('Blockly.Blocks.multimedia');

goog.require('Blockly.Blocks');
goog.require('Blockly.Medias');

Blockly.Blocks['multimedia_audio_play'] = {
  init: function() {
    // Load media list on init
  // Delegate real initialization in ajax callback
    this.setHelpUrl('http://www.erasme.org/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Jouer le son")
         .appendTitle(new Blockly.FieldDropdown(Blockly.Medias.getMediasFor('audio')), "AUDIO");
     this.appendDummyInput()
        .appendTitle(new Blockly.FieldDropdown([
             ["et attendre la fin", "True"],
             ["et passer à la suite", "False"]]), "SYNC");
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

Blockly.Blocks['multimedia_image_play'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(65);
    this.appendDummyInput()
        .appendTitle("Afficher l'image")
        .appendTitle(new Blockly.FieldDropdown(Blockly.Medias.getMediasFor('image')), "IMAGE");
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


Blockly.Blocks['controls_repeat_forever'] = {
  init: function() {
    this.setHelpUrl(Blockly.Msg.CONTROLS_REPEAT_HELPURL);
    this.setColour(120);
    this.appendDummyInput()
        .appendTitle("Jusqu'à la fin des temps")
    this.appendStatementInput('DO')
        .appendTitle("faire");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip(Blockly.Msg.CONTROLS_REPEAT_TOOLTIP);
  }
};
