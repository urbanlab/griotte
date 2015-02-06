Blockly.Blocks['plusdix'] = {
  init: function() {
    this.setHelpUrl('http://www.example.com/');
    this.setColour(285);
    this.appendValueInput("what")
        .setCheck("Number")
        .appendField("10 +");
    this.setInputsInline(true);
    this.setOutput(true, "Number");
    this.setTooltip('');
  }
};
