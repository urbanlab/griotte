'use strict';

goog.provide('Blockly.Python.multimedia');
goog.require('Blockly.Python');

Blockly.Python['multimedia_video'] = function(block) {
  // Search the text for a substring.
  // var operator = block.getTitleValue('END') == 'FIRST' ? 'indexOf' : 'lastIndexOf';
  // var argument0 = Blockly.JavaScript.valueToCode(block, 'FIND',
  //     Blockly.JavaScript.ORDER_NONE) || '\'\'';
  // var argument1 = Blockly.JavaScript.valueToCode(block, 'VALUE',
  //     Blockly.JavaScript.ORDER_MEMBER) || '\'\'';
  // var code = argument1 + '.' + operator + '(' + argument0 + ') + 1';
  // return [code, Blockly.JavaScript.ORDER_MEMBER];
  Blockly.Python.definitions_['from_raspeomix_scenario_multimedia_play_video'] = 'from raspeomix.scenario.multimedia import play_video';

  var media = Blockly.Python.quote_(block.getTitleValue('VIDEO'));
  var code = 'play_video(' + media + ')\n'

  return code;
};

Blockly.Python['multimedia_sound'] = function(block) {
  // Search the text for a substring.
  // var operator = block.getTitleValue('END') == 'FIRST' ? 'indexOf' : 'lastIndexOf';
  // var argument0 = Blockly.JavaScript.valueToCode(block, 'FIND',
  //     Blockly.JavaScript.ORDER_NONE) || '\'\'';
  // var argument1 = Blockly.JavaScript.valueToCode(block, 'VALUE',
  //     Blockly.JavaScript.ORDER_MEMBER) || '\'\'';
  // var code = argument1 + '.' + operator + '(' + argument0 + ') + 1';
  // return [code, Blockly.JavaScript.ORDER_MEMBER];
  Blockly.Python.definitions_['import_raspeomix_scenario_multimedia'] = 'import raspeomix.scenario.multimedia';

  var media = Blockly.Python.quote_(block.getTitleValue('SOUND'));
  var code = 'play_sound(' + media + ')\n'

  return code;
};

Blockly.Python['multimedia_image'] = function(block) {
  // Search the text for a substring.
  // var operator = block.getTitleValue('END') == 'FIRST' ? 'indexOf' : 'lastIndexOf';
  // var argument0 = Blockly.JavaScript.valueToCode(block, 'FIND',
  //     Blockly.JavaScript.ORDER_NONE) || '\'\'';
  // var argument1 = Blockly.JavaScript.valueToCode(block, 'VALUE',
  //     Blockly.JavaScript.ORDER_MEMBER) || '\'\'';
  // var code = argument1 + '.' + operator + '(' + argument0 + ') + 1';
  // return [code, Blockly.JavaScript.ORDER_MEMBER];
  Blockly.Python.definitions_['import_raspeomix_scenario_multimedia'] = 'import raspeomix.scenario.multimedia';

  var duration = Blockly.Python.valueToCode(block, 'DURATION',
    Blockly.Python.ORDER_MULTIPLICATIVE) || '0';

  var media = Blockly.Python.quote_(block.getTitleValue('IMAGE'));
  var code = 'play_image(' + media + ',duration=' + duration + ')\n'

  return code;
};

Blockly.Python['multimedia_volume'] = function(block) {
  // Search the text for a substring.
  // var operator = block.getTitleValue('END') == 'FIRST' ? 'indexOf' : 'lastIndexOf';
  // var argument0 = Blockly.JavaScript.valueToCode(block, 'FIND',
  //     Blockly.JavaScript.ORDER_NONE) || '\'\'';
  // var argument1 = Blockly.JavaScript.valueToCode(block, 'VALUE',
  //     Blockly.JavaScript.ORDER_MEMBER) || '\'\'';
  // var code = argument1 + '.' + operator + '(' + argument0 + ') + 1';
  // return [code, Blockly.JavaScript.ORDER_MEMBER];
  Blockly.Python.definitions_['import_raspeomix_scenario_multimedia'] = 'import raspeomix.scenario.multimedia';

  var volume = Blockly.Python.valueToCode(block, 'VOLUME',
    Blockly.Python.ORDER_MULTIPLICATIVE) || '0';
  volume = Math.min(volume,120);
  var code = 'set_volume(' + volume + ')\n'

  return code;
};
