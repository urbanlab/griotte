'use strict';

goog.provide('Blockly.Medias');

goog.require('Blockly.Toolbox');
goog.require('Blockly.Workspace');

Blockly.Medias.MEDIAS = [];

/**
 * Find all available medias of .
 * @param {string} genre of media to get a list of
 * @return {!Array.<string>} Array of media names.
 */
Blockly.Medias.getMediasFor = function(type) {
  var mediaList = [];
  console.log("Getting medias for " + type);

  this.MEDIAS.forEach(function(element){
  		if(element.filetype === type)
  			mediaList.push([element.filename,element.filepath]);
  });
  //for (var i = Blockly.Medias.MEDIAS[genre].length - 1; i >= 0; i--) {
  //  medialist.push([ Blockly.Medias.MEDIAS[genre][i]['name'], Blockly.Medias.MEDIAS[genre][i]['name'] ]);
  //}
  return mediaList;
};

/**
 * Callback for storage.command.get.medias.* responses
 */
Blockly.Medias.populateMediaList = function(mediaList) {
  console.log(mediaList);
  Blockly.Medias.MEDIAS = mediaList;
};
