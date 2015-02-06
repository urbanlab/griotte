module.exports = function(grunt) {

	grunt.initConfig({

		connect: {
			coverage: {
				options: {
					port: 9001,
					keepalive: true,
					base: 'test/coverage/lcov-report',
					open: true
				}
			}
		},

		mocha: {
			all: {
				src: ['test/test.js']
			}
		},

		watch: {
			all: {
				files: ['lib/*.js', 'test/*.js'],
				tasks: ['mocha'],
				options: {
					atBegin: true
				}
			}
		}
		
	});

	// Run the test and generate the coverage report
	grunt.registerTask('istanbul', function() {
		var done = this.async();
		require('child_process').exec('npm run-script test --coverage', function(err, stdout, stderr) {
			console.error(stderr);
			console.log(stdout);
			console.log('\n\nView test coverage here:');
			console.log('---------------------------');
			console.log('http://localhost:9001');
			done();
		});
	});

	// Register composte tasks
	grunt.util._({
		'default': ['watch'],
		'coverage': ['istanbul', 'connect:coverage']
	}).map(function(task, name) {
		grunt.registerTask(name, task);
	});

	// Register npm tasks
	[
		'grunt-contrib-connect',
		'grunt-contrib-watch',
		'grunt-mocha-istanbul-coveralls'
	].forEach(grunt.loadNpmTasks);

	//grunt.loadTasks('tasks');

};
