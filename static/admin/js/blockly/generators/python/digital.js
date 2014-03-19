'use strict';

goog.provide('Blockly.Python.digital');
goog.require('Blockly.Python');

Blockly.Python['digital_sensor'] = function(block) {
  var port = Blockly.Python.quote_(block.getTitleValue('CHANNEL'));
  var profile = Blockly.Python.quote_(block.getTitleValue('PROFILE'));

  Blockly.Python.definitions_['from_griotte_scenario_digital_get_digital'] = 'from griotte.scenario.digital import get_digital';

  var code = 'get_digital(' + port.toLowerCase() + ')'
  console.log(code)

  return [code, Blockly.Python.ORDER_MEMBER];
};

Blockly.Python['digital_sensor_edge'] = function(block) {
  var port = Blockly.Python.quote_(block.getTitleValue('CHANNEL').toLowerCase());
  var edge = Blockly.Python.quote_(block.getTitleValue('EDGE').toLowerCase());

  Blockly.Python.definitions_['from_griotte_scenario_digital_wait_edge'] = 'from griotte.scenario.digital import wait_edge';

  var code = 'wait_edge('  + port +  ', ' + edge + ')'

  return [code, Blockly.Python.ORDER_MEMBER];
};
