'use strict';

goog.provide('Blockly.Medias');

goog.require('Blockly.Toolbox');
goog.require('Blockly.Workspace');

Blockly.Medias.MEDIAS = {};

/**
 * Find all available medias of .
 * @param {string} genre of media to get a list of
 * @return {!Array.<string>} Array of media names.
 */
Blockly.Medias.getMediasFor = function(genre) {
  var medialist = [];
  console.log("Getting medias for " + genre);

  if (! genre in Blockly.Medias.MEDIAS) {
    return [];
  }

  for (var i = Blockly.Medias.MEDIAS[genre].length - 1; i >= 0; i--) {
    medialist.push([ Blockly.Medias.MEDIAS[genre][i]['name'], Blockly.Medias.MEDIAS[genre][i]['name'] ]);
  }
  return medialist;
};

/**
 * Callback for store.command.get.medias.* responses
 */
Blockly.Medias.callbackMedias = function(medialist) {
  console.log(medialist.data.value);
  Blockly.Medias.MEDIAS = medialist.data.value;
};
