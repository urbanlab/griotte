'use strict';

goog.provide('Blockly.Python.analog');
goog.require('Blockly.Python');

Blockly.Python['capteur_analogique'] = function(block) {
  // Search the text for a substring.
  // var operator = block.getTitleValue('END') == 'FIRST' ? 'indexOf' : 'lastIndexOf';
  // var argument0 = Blockly.JavaScript.valueToCode(block, 'FIND',
  //     Blockly.JavaScript.ORDER_NONE) || '\'\'';
  // var argument1 = Blockly.JavaScript.valueToCode(block, 'VALUE',
  //     Blockly.JavaScript.ORDER_MEMBER) || '\'\'';
  // var code = argument1 + '.' + operator + '(' + argument0 + ') + 1';
  // return [code, Blockly.JavaScript.ORDER_MEMBER];
  var code = 'print("Python generator for capteur_analogique")'
  console.log(code)
  return [code, Blockly.Python.ORDER_MEMBER];
};
