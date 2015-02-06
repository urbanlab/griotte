'use strict';

goog.provide('Blockly.Python.misc');
goog.require('Blockly.Python');

Blockly.Python['misc_wait'] = function(block) {
  Blockly.Python.definitions_['from_time_sleep'] = 'from time import sleep';

  var duration = Blockly.Python.valueToCode(block, 'DURATION',
    Blockly.Python.ORDER_MULTIPLICATIVE) || '0';

  var code = 'sleep(' + duration + ')\n';

  return code;
};

Blockly.Python['misc_volume'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_storage_set_volume'] = 'from griotte.scenario.storage import set_volume';

  var volume = Blockly.Python.valueToCode(block, 'VOLUME',
    Blockly.Python.ORDER_MULTIPLICATIVE) || '0';
  volume = Math.min(volume,120);
  var code = 'set_volume(' + volume + ')\n'

  return code;
};
