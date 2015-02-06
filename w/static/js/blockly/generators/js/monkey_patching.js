
Blockly.JavaScript['controls_repeat_forever'] = function(block) {
  var branch = Blockly.JavaScript.statementToCode(block, 'DO');
  var code = 'while (true) {\n' + branch + '\n}';
  return code;
};

// override window.alert with api function
Blockly.JavaScript['text_print'] = function(block) {
  // Print statement.
  var argument0 = Blockly.JavaScript.valueToCode(block, 'TEXT',
      Blockly.JavaScript.ORDER_NONE) || '\'\'';
  return 'print(' + argument0 + ');\n';
};
