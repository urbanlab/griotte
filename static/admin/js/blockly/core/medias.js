'use strict';

goog.provide('Blockly.Medias');

goog.require('Blockly.Toolbox');
goog.require('Blockly.Workspace');

Blockly.Medias.MEDIAS = {};

/**
 * Find all available medias of .
 * @param {string} type of media to get a list of
 * @return {!Array.<string>} Array of media names.
 */
Blockly.Medias.getMediasFor = function(type) {
  var medialist = [];
  for (var i = Blockly.Medias.MEDIAS[type].length - 1; i >= 0; i--) {
    medialist.push([ Blockly.Medias.MEDIAS[type][i]['name'], Blockly.Medias.MEDIAS[type][i]['name'] ]);
  }
  return medialist;
};

/**
 * Callback for store.command.get.medias.* responses
 */
Blockly.Medias.callbackMedias = function(medialist) {
  Blockly.Medias.MEDIAS = medialist.data.value;
};
