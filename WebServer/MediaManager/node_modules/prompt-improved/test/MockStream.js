var util = require('util'),
	stream = require('stream');

var MockStream = function() {
	var me = this;
	this.on('pipe', function (src) {
		src.on('data', function (d) {
			me.emit('data', d+'');
		});
	});
};
util.inherits(MockStream, stream.Stream);

var msProto = MockStream.prototype;
msProto.resume = msProto.pause = msProto.end = function() {}; 

MockStream.prototype.write = function(data) {
	this.emit('data', data);
	return true;
};

module.exports = MockStream;
