// link : https://blockly-demo.appspot.com/static/demos/blockfactory/index.html#fjfvoe

Blockly.JavaScript['plusdix'] = function(block) {
  var value_what = Blockly.JavaScript.valueToCode(block, 'what', Blockly.JavaScript.ORDER_ATOMIC);
  // TODO: Assemble JavaScript into code variable.
  var code = parseInt(value_what) + 10;
  // TODO: Change ORDER_NONE to the correct strength.
  return [code, Blockly.JavaScript.ORDER_NONE];
};
