Blockly.JavaScript['settimeout'] = function(block) {
  var value_time = Blockly.JavaScript.valueToCode(block, 'time', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable_handler = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('handler'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble JavaScript into code variable.
  var code = variable_handler+' = setTimeout(function(){\n'+statements_callback+'},'+value_time+');\n';
  return code;
};

Blockly.JavaScript['cleartimeout'] = function(block) {
  var variable_handler = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('handler'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble JavaScript into code variable.
  var code = 'clearTimeout('+variable_handler+');\n';
  return code;
};

Blockly.JavaScript['setinterval'] = function(block) {
  var value_time = Blockly.JavaScript.valueToCode(block, 'time', Blockly.JavaScript.ORDER_ATOMIC);
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable_handler = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('handler'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble JavaScript into code variable.
  var code = variable_handler+' = setInterval(function(){\n'+statements_callback+'}\n,'+value_time+');\n';
  return code;
};

Blockly.JavaScript['clearinterval'] = function(block) {
  var variable_handler = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('handler'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble JavaScript into code variable.
  var code = 'clearInterval('+variable_handler+');\n';
  return code;
};
