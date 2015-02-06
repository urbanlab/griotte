var Prompt = require('../lib/index.js'),
	MockStream = require('./MockStream.js'),
	assert = require('assert'),
	chalk = require('chalk');

// Force colors to be on
chalk.enabled = true;

describe('#Prompt', function() {

	describe('Prompt()', function() {

		it('should return a new instance with or without the new operator', function() {
			var p1 = Prompt();
			assert.ok(p1 instanceof Prompt, 'Should return a new instance without the new operator');

			var p2 = new Prompt();
			assert.ok(p2 instanceof Prompt, 'Should return a new instance with the new operator');
		});

		it('should have the correct default options', function() {
			assert.equal(Prompt.defaultOptions.prefix, '');
			assert.equal(Prompt.defaultOptions.suffix, ': ');
			assert.equal(Prompt.defaultOptions.defaultPrefix, ' (');
			assert.equal(Prompt.defaultOptions.defaultSuffix, ')');
			assert.equal(Prompt.defaultOptions.inputError, 'Error encountered, try again.');
			assert.equal(Prompt.defaultOptions.requiredError, 'Required! Try again.');
			assert.equal(Prompt.defaultOptions.invalidError, 'Invalid input: ');
			assert.equal(Prompt.defaultOptions.attemptsError, 'Maximum attempts reached!');
		});

		it('should set options when passed in', function() {
			var p = Prompt({prefix: '>>', inputError: 'Generic error...'});
			assert.equal(p.options.prefix, '>>', 'Should override options when passed into the constructor.');
			assert.equal(p.options.inputError, 'Generic error...', 'Should override options when passed into the constructor.');
		});

		it('should set the input and output streams', function(done) {
			var input = new MockStream(),
				output = new MockStream();

			output.on('data', function(data) {
				assert.equal(data, 'Test Out!!!');
				p.options.stdin.write('Test In!!!');
			});
			input.on('data', function(data) {
				assert.equal(data, 'Test In!!!');
				done();
			});

			var p = new Prompt({
				stdin: input,
				stdout: output
			});
			p.options.stdout.write('Test Out!!!');
			
		});

		it('should throw if errors occure getting the input', function(done) {

			var p = new Prompt({
				stdin: new MockStream(),
				stdout: new MockStream(),
				stderr: new MockStream(),
				timeout: 5
			});

			p.ask('Sup?', function (err, res) {
				assert.equal(err, 'Error: timed out', 'Did not throw an error when response did not come in time');
				done();
			});

		});
		
	});

	describe('Prompt attributes', function() {

		it('should have chalk embeded', function() {
			assert(Prompt.chalk, 'Did not include chalk');
		});

		it('should have boolean helpers', function() {
			assert(Prompt.isBool, 'Did not have isBool regex');
			assert(Prompt.filterBool, 'Did not have filterBool function');

			assert(Prompt.isBool.test('y'), 'Did not evaluate y as a boolean response');
			assert(Prompt.isBool.test('yes'), 'Did not evaluate yes as a boolean response');
			assert(Prompt.isBool.test('n'), 'Did not evaluate n as a boolean response');
			assert(Prompt.isBool.test('no'), 'Did not evaluate no as a boolean response');

			assert.equal(Prompt.filterBool('y'), true, 'Did not correctly convert y to true');
			assert.equal(Prompt.filterBool('yes'), true, 'Did not correctly convert yes to true');
			assert.equal(Prompt.filterBool('n'), false, 'Did not correctly convert n to false');
			assert.equal(Prompt.filterBool('no'), false, 'Did not correctly convert no to false');
		});
	});

	describe('prompt.ask()', function() {

		var prompt,
			input = new MockStream(),
			output = new MockStream(),
			error = new MockStream();

		beforeEach(function() {
			prompt = new Prompt({
				stdin: input,
				stdout: output,
				stderr: error
			});
		});

		describe('Asking a single question', function() {

			it('should throw if either question or callback are not defined', function(done) {
				assert.throws(function() {
					prompt.ask();
				}, TypeError, 'Did not throw when both question and callback were not defined');
				done();
			});

			it('should throw if question is not defined', function(done) {
				assert.throws(function() {
					prompt.ask(undefined, function(){});
				}, TypeError, 'Did not throw when a question was not defined');
				done();
			});

			it('should throw if callback is not defined', function(done) {
				assert.throws(function() {
					prompt.ask('Test', undefined);
				}, TypeError, 'Did not throw when a callback was not defined');
				done();
			});

			it('should ask a single question with no options', function(done) {

				output.once('data', function(d) {
					assert.equal(d, '\x1b[1mWho d f are u?\x1b[22m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
				});

				prompt.ask('Who d f are u?', function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'Test input.', 'Input did not match');
					done();
				});
				process.nextTick(function() {
					input.write('Test input.\n');
				});
				
			});

			it('should ask a single question with options', function(done) {

				output.once('data', function(d) {
					assert.equal(d, '\x1b[37m[?] \x1b[39m\x1b[1mWho let the dogs out?\x1b[22m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
				});

				prompt.ask('Who let the dogs out?', {
					prefix: '[?] '
				}, function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'Test input.', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('Test input.\n');
				});
			});

			it('should ask a single question with the question defined in the options', function(done) {

				output.once('data', function(d) {
					assert.equal(d, '\x1b[37m[?] \x1b[39m\x1b[1mWho let the dogs out?\x1b[22m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
				});

				prompt.ask({
					question: 'Who let the dogs out?',
					prefix: '[?] '
				}, function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'Test input.', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('Test input.\n');
				});

			});

			it('should work just fine with no suffix defined', function(done) {

				output.once('data', function(d) {
					assert.equal(d, '\x1b[1mNo suffix\x1b[22m ', 'Did not output the proper question');
				});

				prompt.ask({
					question: 'No suffix',
					suffix: ''
				}, function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'Test input.', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('Test input.\n');
				});

			});

			it('should handel boolean questions', function(done) {

				prompt.ask({
					question: 'Yes or no?',
					boolean: true
				}, function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, true, 'Input was not true as was expected');
					done();
				});
				
				process.nextTick(function() {
					input.write('Test input.\n');
					process.nextTick(function() {
						input.write('y\n');
					});
				});

			});
		});

		describe('Asking multiple questions', function() {

			it('should ask multiple question when passed an array as the first param', function(done) {
				
				output.once('data', function(d) {
					assert.equal(d, '\x1b[1mWhere in the world is Carmen Sandiego?\x1b[22m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
					output.once('data', function(d) {
						assert.equal(d, '\x1b[1mMore stupid questions.\x1b[22m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
					});
				});

				prompt.ask([{
					question: 'Where in the world is Carmen Sandiego?'
				}, {
					question: 'More stupid questions.'
				}], function(err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res['Where in the world is Carmen Sandiego?'], 'Soviet Russia', 'Input did not match');
					assert.equal(res['More stupid questions.'], 'Yes, more', 'Input did not match');
					done();
				});

				process.nextTick(function() {
					input.write('Soviet Russia\n');
					process.nextTick(function() {
						input.write('Yes, more\n');
					});
				});

			});
			
			it('should assign question answers to key if it exists, otherwise the question text', function(done) {

				prompt.ask([{
					question: 'Question text',
					key: 'ask'
				}, {
					question: 'Question text'
				}], function (err, res) {
					assert.equal(res['ask'], 'y', 'Did not use key for when provided');
					assert.equal(res['Question text'], 'y', 'Did not use question text when key not provided');
					done();
				});
				
				process.nextTick(function() {
					input.write('y\n');
					process.nextTick(function() {
						input.write('y\n');
					});
				});

			});

			it('should accumulate errors if they happen', function(done) {
				
				prompt.ask([{
					question: 'Question text',
					key: 'ask',
					attempts: 1,
					required: true
				}, {
					question: 'Question text',
					attempts: 1,
					required: true
				}], function (err, res) {
					assert.equal(err['ask'], 'Maximum attempts reached!', 'Did not store error by key');
					assert.equal(err['Question text'], 'Maximum attempts reached!', 'Did not store error by question');
					done();
				});
				
				process.nextTick(function() {
					input.write('\n');
					process.nextTick(function() {
						input.write('\n');
						process.nextTick(function() {
							input.write('\n');
							process.nextTick(function() {
								input.write('\n');
							});
						});
					});
				});

			});

			it('should ask for confirmation', function(done) {
				
				prompt.ask([{
					question: 'Question 1'
				}, {
					question: 'Question 2',
					key: 2
				}], {
					confirm: true
				}, function (err, res) {
					done();
				});
				
				process.nextTick(function() {
					input.write('Answer 1\n');
					process.nextTick(function() {
						input.write('Answer 2\n');
						process.nextTick(function() {
							input.write('N\n');
							process.nextTick(function() {
								input.write('Answer 12\n');
								process.nextTick(function() {
									input.write('Answer 22\n');
									process.nextTick(function() {
										input.write('yes\n');
									});
								});
							});
						});
					});
				});

			});

		});

		describe('Prompt features', function() {

			it('should require answers', function(done) {

				error.once('data', function(d) {
					assert.equal(d, '\x1b[31mRequired! Try again.\x1b[39m', 'did not output the required error message');

					process.nextTick(function() {
						input.write('Some Input\n');
					});
				});

				prompt.ask('Required question', {
					required: true
				}, function (err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'Some Input', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('\n');
				});

			});

			it('should limit attempts', function(done) {

				prompt.ask('Limited reqponses', {
					required: true,
					attempts: 3
				}, function (err, res) {
					assert.equal(err, 'Maximum attempts reached!', 'Did not thorw the right error');
					assert.equal(res, '', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('\n');
					process.nextTick(function() {
						input.write('\n');
						process.nextTick(function() {
							input.write('\n');
						});
					});
				});

			});

			it('should display and submit the default', function(done) {

				output.once('data', function(d) {
					assert.equal(d, '\x1b[1mDefault responses\x1b[22m\x1b[37m (default)\x1b[39m\x1b[37m: \x1b[39m ', 'Did not output the proper question');
				});

				prompt.ask('Default responses', {
					default: 'default'
				}, function (err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					assert.equal(res, 'default', 'Input did not match');
					done();
				});
				
				process.nextTick(function() {
					input.write('\n');
				});
			});

			it('should validate the input with a function', function(done) {

				error.once('data', function(d) {
					assert.equal(d, '\x1b[31mInvalid input: Wrong input\x1b[39m', 'Did not output the invalid input error message');
				});

				prompt.ask('Valid input', {
					validate: function(input) {
						return input == 'Test Input';
					}
				}, function (err, res) {
					assert.equal(err, null, 'Threw an error...hmmmm');
					done();
				});
				
				process.nextTick(function() {
					input.write('Wrong input\n');
					process.nextTick(function() {
						input.write('Test Input\n');
					});
				});

			});

			it('should validate the input with a regular expression', function(done) {

				error.once('data', function(d) {
					assert.equal(d, '\x1b[31mInvalid input: a\x1b[39m', 'Did not output the invalid input error message');
				});

				prompt.ask('Validate input', {
					validate: /^[0-9]+$/
				}, function (err, res) {
					assert.equal(res, '1', 'Input not collected correctly');
					done();
				});
				
				process.nextTick(function() {
					input.write('a\n');
					process.nextTick(function() {
						input.write('1\n');
					});
				});

			});

			it('should run a filter before validation', function(done) {

				prompt.ask('Filtered input', {
					validate: /^Abc$/,
					before: function(val) {
						return val.charAt(0).toUpperCase() + val.slice(1);
					},
				}, function (err, res) {
					assert.equal(res, 'Abc', 'Input not collected correctly');
					done();
				});
				
				process.nextTick(function() {
					input.write('abc\n');
				});

			});

			it('should run a filter after validation', function(done) {

				prompt.ask('Filtered input', {
					validate: /^(?:y(?:es)?|n(?:o)?)$/i,
					after: function(value) {
						value = value.toLowerCase();
						if (value === 'y' || value === 'yes') return true;
						return false;
					}
				}, function (err, res) {
					assert.equal(res, true, 'Input not filtered correctly');
					done();
				});
				
				process.nextTick(function() {
					input.write('y\n');
				});

			});

			it('should ask questions depending on previous input', function(done) {

				prompt.ask([{
					question: 'ask'
				}, {
					question: 'Should be asked',
					depends: function(input) {
						return !!input.ask;
					}
				}, {
					question: 'Should not be asked',
					depends: function(input) {
						return !input.ask;
					}
				}, {
					question: 'Should also be asked',
					depends: true
				}, {
					question: 'Should never be asked',
					depends: false
				}], function (err, res) {
					assert.equal(res['ask'], 'y', 'Input not collected correctly');
					assert.equal(res['Should be asked'], 'y', 'Did not ask question that should have been asked');
					assert.equal(res['Should also be asked'], 'y', 'Did not ask question that should have been asked because boolean true was passed to depends');
					assert.equal(res['Should not be asked'], undefined, 'Asked question that shouldn\'t have been asked');
					assert.equal(res['Should never be asked'], undefined, 'Asked a question when boolean false was passed to depends');
					done();
				});
				
				process.nextTick(function() {
					input.write('y\n');
					process.nextTick(function() {
						input.write('y\n');
						process.nextTick(function() {
							input.write('y\n');
						});
					});
				});

			});

		});
		
	});
	
});
