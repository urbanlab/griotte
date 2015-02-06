'use strict';

goog.provide('Blockly.Python.analog');
goog.require('Blockly.Python');

Blockly.Python['analog_sensor'] = function(block) {
  var channel = Blockly.Python.valueToCode(block, 'CHANNEL',
    Blockly.Python.ORDER_MULTIPLICATIVE) || 'wtf';

  var profile = Blockly.Python.valueToCode(block, 'PROFILE',
    Blockly.Python.ORDER_MULTIPLICATIVE) || 'wtf again';

  // We need to import few stuff at init time
  Blockly.Python.definitions_['from_griotte_scenario_analog_set_profile'] = 'from griotte.scenario.analog import set_profile';

  Blockly.Python.definitions_['from_griotte_scenario_analog_get_analog'] = 'from griotte.scenario.analog import get_analog';

  channel = Blockly.Python.quote_(block.getTitleValue('CHANNEL'));
  profile = Blockly.Python.quote_(block.getTitleValue('PROFILE'));

  // We need to set the profile once for all
  Blockly.Python.definitions_['griotte_scenario_analog_set_profile'] = 'set_profile(' + channel + ',' + profile + ')';

  var code = 'get_analog(' + channel + ')'

  return [code, Blockly.Python.ORDER_MEMBER];
};
