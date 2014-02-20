'use strict';

goog.provide('Blockly.Python.digital');
goog.require('Blockly.Python');

Blockly.Python['digital_sensor'] = function(block) {
  var port = Blockly.Python.quote_(block.getTitleValue('CHANNEL'));
  var profile = Blockly.Python.quote_(block.getTitleValue('PROFILE'));

  // We need to import few stuff at init time
  //Blockly.Python.definitions_['from_griotte_scenario_digital_set_profile'] = 'from griotte.scenario.digital import set_profile';

  Blockly.Python.definitions_['from_griotte_scenario_digital_get_digital'] = 'from griotte.scenario.digital import get_digital';

  var code = 'get_digital(' + port.toLowerCase() + ')'
  console.log(code)

  return [code, Blockly.Python.ORDER_MEMBER];
};
