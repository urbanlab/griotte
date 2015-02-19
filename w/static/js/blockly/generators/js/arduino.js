Blockly.JavaScript['fonanalog'] = function(block) {
  var dropdown_pin = block.getFieldValue('pin');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'fonAnalog('+dropdown_pin+',function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};

Blockly.JavaScript['fwritedigital'] = function(block) {
  var dropdown_valeur = block.getFieldValue('valeur');
  var dropdown_pin = block.getFieldValue('pin');
  // TODO: Assemble JavaScript into code variable.
  var code = 'fwriteDigital('+dropdown_pin+','+dropdown_valeur+');';
  return code;
};


Blockly.JavaScript['fondigitalchange'] = function(block) {
  var dropdown_pin = block.getFieldValue('pin');
  var statements_callback = Blockly.JavaScript.statementToCode(block, 'callback');
  var variable0 = Blockly.JavaScript.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
  var code = 'fonDigitalChange('+dropdown_pin+',function('+variable0+'){\n'+statements_callback+'});\n';
  return code;
};

Blockly.JavaScript['fwriteservo'] = function(block) {
  var value_angle = Blockly.JavaScript.valueToCode(block, 'angle', Blockly.JavaScript.ORDER_ATOMIC);
  var dropdown_pin = block.getFieldValue('pin');
  if(value_angle > 180) value_angle = 180;
  if(value_angle < 0 ) value_angle = 0;
  var code = 'fwriteServo('+dropdown_pin+','+value_angle+');';
  return code;
};

Blockly.JavaScript['fwritepwm'] = function(block) {
  var value_valeur = Blockly.JavaScript.valueToCode(block, 'valeur', Blockly.JavaScript.ORDER_ATOMIC);
  var dropdown_pin = block.getFieldValue('pin');
  if(value_valeur > 255) value_valeur = 255;
  if(value_valeur < 0 ) value_valeur = 0;
  var code = 'fwritePWM('+dropdown_pin+','+value_valeur+');';
  return code;
};