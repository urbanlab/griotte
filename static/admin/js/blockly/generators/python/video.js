'use strict';

goog.provide('Blockly.Python.multimedia');
goog.require('Blockly.Python');

Blockly.Python['video_play'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_multimedia_play_video'] = 'from griotte.scenario.multimedia import play_video';

  var media = Blockly.Python.quote_(block.getTitleValue('VIDEO'));
  var code = 'play_video(' + media + ', sync=' + block.getTitleValue('SYNC') + ')\n'

  return code;
};

Blockly.Python['video_stop'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_multimedia_stop_video'] = 'from griotte.scenario.multimedia import stop_video';

  return 'stop_video()\n';
};



