'use strict';

goog.provide('Blockly.Blocks.rfid');
goog.require('Blockly.Blocks');

Blockly.Blocks['rfid_read'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org');
    this.setColour(349);
    this.appendDummyInput()
        .appendField("Lire un tag RFID ")
    this.setTooltip('RFID Tag');
    this.setOutput(true);
  },
};

Blockly.Blocks['rfid_wait_for'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org');
    this.setColour(349);
    this.appendValueInput("TAG")
        .setCheck("RFIDTag")
        .appendField("Lire le tag");
    this.setInputsInline(true);
    this.setTooltip('RFID Tag');
    this.setOutput(true);
  },
};

Blockly.Blocks['rfid_tag'] = {
  init: function() {
    this.setHelpUrl('http://www.erasme.org');
    this.setColour(349);
    this.appendDummyInput()
        .appendField("n°")
        .appendField(new Blockly.FieldTextInput(''), 'TAG')
    this.setTooltip('RFID Tag #');
    this.setOutput(true, 'RFIDTag');

    // This sux big time
    //Griotte.subscribe("rfid.event.tag", Blockly.Blocks['rfid_tag'].setRFID.bind(this))
  },
  setRFID: function(message) {
    console.log(this);
    console.log(Blockly.selected);
    if (Blockly.selected == this) {
        this.setFieldValue(message.data.tag.toLowerCase(), 'TAG');
    }
  }
};
