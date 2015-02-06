var serialport = require("serialport");
var SerialPort = serialport.SerialPort

var arduinoPort;

serialport.list(function (err, ports) {
  ports.forEach(function(port) {
    //console.log(port.comName);
    //console.log(port.pnpId);
    //console.log(port.manufacturer);
    if(port.pnpId.indexOf("Arduino") > -1){
    	console.log(port.pnpId.indexOf("Arduino"))
    	arduinoPort = port.comName;
    	console.log(arduinoPort);
    	
    	var serialPort = new SerialPort(arduinoPort, {
		  baudrate: 9600,
		  parser: serialport.parsers.readline("\n")
		},false);
		serialPort.open(function () {
		  console.log('open');
		  serialPort.on('data', function(data) {
			console.log(data);
		  });
		  //serialPort.write("ls\n", function(err, results) {
		  //  console.log('err ' + err);
		  //  console.log('results ' + results);
		  //});
		});
    	return;
    }
  });
});


