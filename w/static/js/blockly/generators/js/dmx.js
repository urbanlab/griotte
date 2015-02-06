
Blockly.JavaScript['dmx_send_single'] = function(block) {
  var value = Blockly.JavaScript.valueToCode(block, 'VALUE', Blockly.JavaScript.ORDER_ATOMIC);
  var channel = Blockly.JavaScript.valueToCode(block, 'CHANNEL', Blockly.JavaScript.ORDER_ATOMIC);
  var code = 'sendDmx(' + channel + ', ' + value + ');\n'

  return code;
};

Blockly.JavaScript['dmx_send_channels'] = function(block) {
  var values = Blockly.JavaScript.valueToCode(block, 'VALUES', Blockly.JavaScript.ORDER_ATOMIC).replace(/ /g, "");
  values = values.substring(1,values.length-1);
  var valuesArray = values.split(",");
  
  var channels = Blockly.JavaScript.valueToCode(block, 'CHANNELS', Blockly.JavaScript.ORDER_ATOMIC).replace(/ /g, "");
  channels = channels.substring(1,channels.length-1); 
  var channelsArray = channels.split(",");
  
  
  var valuesObj = {};
  for(var k=0;k<channelsArray.length;k++){
  	if(k>valuesArray.length-1 || isNaN(valuesArray[k]))
  		valuesObj[channelsArray[k]] = 0;
  	else
  		valuesObj[channelsArray[k]] = parseInt(valuesArray[k]);
  }
  var code = "sendDmxM('"+JSON.stringify(valuesObj)+"');\n"
  return code;
};

Blockly.JavaScript['dmx_blackout'] = function(block) {
  var code = 'sendDmxBlackout();\n'
  return code;
};



