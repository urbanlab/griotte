goog.require('Blockly.Blocks');

Blockly.Blocks['controls_repeat_forever'] = {
  init: function() {
    this.setHelpUrl(Blockly.Msg.CONTROLS_REPEAT_HELPURL);
    this.setColour(120);
    this.appendDummyInput()
        .appendTitle("Jusqu'à la fin des temps")
    this.appendStatementInput('DO')
        .appendTitle("faire");
    this.setPreviousStatement(true);
    this.setNextStatement(true);
    this.setTooltip(Blockly.Msg.CONTROLS_REPEAT_TOOLTIP);
  }
};
