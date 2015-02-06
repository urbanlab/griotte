'use strict';

goog.provide('Blockly.Python.image');
goog.require('Blockly.Python');

Blockly.Python['image_play'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_image_play_image'] = 'from griotte.scenario.image import play_image';

  var duration = Blockly.Python.valueToCode(block, 'DURATION',
    Blockly.Python.ORDER_MULTIPLICATIVE) || '0';

  var media = Blockly.Python.quote_(block.getTitleValue('IMAGE'));
  var code = 'play_image(' + media + ',duration=' + duration + ')\n'

  return code;
};

Blockly.Python['image_set_background'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_image_set_background'] = 'from griotte.scenario.image import set_background';

  var color = Blockly.Python.valueToCode(block, 'COLOR',
    Blockly.Python.ORDER_MULTIPLICATIVE) || "'#000000'";

  var code = 'set_background(' + color + ')\n';
  return code;
};

