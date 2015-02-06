Blockly.JavaScript['readanalog'] = function(block) {
  var dropdown_channel = block.getFieldValue('channel');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  // TODO: Assemble JavaScript into code variable.
  var code = 'readAnalog('+dropdown_channel+',function('+variable0+'){\n'+statements_callback+'});\n';
  //return [code, Blockly.JavaScript.ORDER_NONE];
  return code;
};

Blockly.JavaScript['onanalog'] = function(block) {
  var dropdown_channel = block.getFieldValue('channel');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'onAnalog('+dropdown_channel+',function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};

Blockly.JavaScript['readdigital'] = function(block) {
  var dropdown_channel = block.getFieldValue('channel');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'readDigital("'+dropdown_channel+'",function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};

Blockly.JavaScript['writedigital'] = function(block) {
  var dropdown_valeur = block.getFieldValue('valeur');
  var dropdown_channel = block.getFieldValue('channel');
  // TODO: Assemble JavaScript into code variable.
  var code = 'writeDigital("'+dropdown_channel+'",'+dropdown_valeur+');';
  return code;
};

Blockly.JavaScript['ondigital'] = function(block) {
  var dropdown_channel = block.getFieldValue('channel');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'onDigital("'+dropdown_channel+'",function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};

Blockly.JavaScript['ondigitalchange'] = function(block) {
  var dropdown_channel = block.getFieldValue('channel');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'onDigitalChange("'+dropdown_channel+'",function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};
