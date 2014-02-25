goog.require('Blockly.Python');

Blockly.Python['controls_repeat_forever'] = function(block) {
  var branch = Blockly.Python.statementToCode(block, 'DO') || '  pass\n';

  var code = 'while (True):\n' + branch;
  return code;
};
