'use strict';

goog.provide('Blockly.Python.video');
goog.require('Blockly.Python');

Blockly.Python['video_play'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_video_play_video'] = 'from griotte.scenario.video import play_video';

  var media = Blockly.Python.quote_(block.getTitleValue('VIDEO'));
  var code = 'play_video(' + media + ', sync=' + block.getTitleValue('SYNC') + ')\n'

  return code;
};

Blockly.Python['video_stop'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_video_stop_video'] = 'from griotte.scenario.video import stop_video';

  return 'stop_video()\n';
};



