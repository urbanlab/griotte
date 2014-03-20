'use strict';

goog.provide('Blockly.Python.rfid');
goog.require('Blockly.Python');

Blockly.Python['rfid_read'] = function(block) {
  Blockly.Python.definitions_['from_griotte_scenario_rfid_read'] = 'from griotte.scenario.digital import rfid_read';

  var code = 'rfid_read(None)\n'
  console.log(code)

  return [code, Blockly.Python.ORDER_FUNCTION_CALL];
};

Blockly.Python['rfid_wait_for'] = function(block) {
  var tag = Blockly.Python.valueToCode(block, 'TAG', Blockly.Python.ORDER_ATOMIC);

  var code = 'rfid_read(' + tag + ')\n'
  return code;
};

Blockly.Python['rfid_tag'] = function(block) {
  // Text value.
  var code = Blockly.Python.quote_(block.getFieldValue('TAG'));
  return [code, Blockly.Python.ORDER_ATOMIC];
};
