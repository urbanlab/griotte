'use strict';

goog.provide('Blockly.Python.audio');
goog.require('Blockly.Python');

Blockly.Python['audio_play'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_audio_play_audio'] = 'from griotte.scenario.audio import play_audio';

  var media = Blockly.Python.quote_(block.getTitleValue('AUDIO'));
  var code = 'play_audio(' + media + ', sync=' + block.getTitleValue('SYNC') + ')\n'

  return code;
};

Blockly.Python['audio_stop'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_multimedia_stop_audio'] = 'from griotte.scenario.audio import stop_audio';

  return 'stop_audio()\n';
};

