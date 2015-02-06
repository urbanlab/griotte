var Mocha = require('mocha');

module.exports = function(grunt) {

	// Default Options
	var defaultOptions = {
		grep: '',
		ui: 'bdd',
		reporter: 'dot',
		timeout: 2000
	};

	grunt.registerMultiTask('mocha', 'A mocha test runner for node', function() {

		// Async task
		done = this.async();

		// Merge config with defaults
		var options = grunt.util._.extend(defaultOptions, this.options());

		// Log options
		grunt.verbose.writeflags(options, 'Options');

		// Create mocha instance
		var mocha = new Mocha(options);

		// Add the files
		this.filesSrc.forEach(function(file) {
			mocha.addFile(file);
		});

		// Run the tests
		mocha.run(function(fails) {
			process.exit(function() {
				process.exit(fails);
				done();
			});
		});

	});

};
