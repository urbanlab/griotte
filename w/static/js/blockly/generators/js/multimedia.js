'use strict';

//goog.provide('Blockly.Python.video');
//goog.require('Blockly.Python');

Blockly.JavaScript['video_play'] = function(block) {
	var checkbox_loop_cb = block.getFieldValue('loop_cb') == 'TRUE';
  var media = Blockly.JavaScript.quote_(block.getTitleValue('VIDEO'));
  if(checkbox_loop_cb)
  	var code = 'playMediaLoop(' + media + ');\n';
  else
  	var code = 'playMedia(' + media + ');\n';
  return code;
};

Blockly.JavaScript['video_pause'] = function(block) {
  return 'pauseMedia();\n';
};

Blockly.JavaScript['video_resume'] = function(block) {
  return 'resumeMedia();\n';
};

Blockly.JavaScript['video_stop'] = function(block) {
  return 'stopMedia();\n';
};

Blockly.JavaScript['image_play'] = function(block) {
  var media = Blockly.JavaScript.quote_(block.getTitleValue('IMAGE'));
  var code = 'playMedia(' + media + ');\n';
  return code;
};

Blockly.JavaScript['audio_play'] = function(block) {
	var checkbox_loop_cb = block.getFieldValue('loop_cb') == 'TRUE';
  var media = Blockly.JavaScript.quote_(block.getTitleValue('AUDIO'));
  if(checkbox_loop_cb)
  	var code = 'playMediaLoop(' + media + ');\n';
  else
  	var code = 'playMedia(' + media + ');\n';
  return code;
};
Blockly.JavaScript['audio_stop'] = function(block) {
  return 'stopMedia();\n';
};

