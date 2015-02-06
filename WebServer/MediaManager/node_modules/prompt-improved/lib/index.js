// Requirements
var readline = require('readline'),
	chalk = require('chalk'),
	read = require('read');

// Utility extend
function extend(obj) {
	var args = Array.prototype.slice.call(arguments, 1);
	for (var i = 0, len = args.length; i < len; i++) {
		if (args[i]) {
			for (var prop in args[i]) {
				obj[prop] = args[i][prop];
			}
		}
	}
    return obj;
};

// Constructor
var Prompt = function(options) {

	// Make sure this is a new instance of the prompt
	if (!(this instanceof Prompt))
		return new Prompt(options);

	// Merge options
	this.options = extend({}, Prompt.defaultOptions, options);
};

// Default options
Prompt.defaultOptions = {
	prefix           : '',
	suffix           : ': ',
	defaultPrefix    : ' (',
	defaultSuffix    : ')',
	textTheme        : chalk.bold,
	prefixTheme      : chalk.white,
	suffixTheme      : chalk.white,
	defaultTheme     : chalk.white,
	inputError       : 'Error encountered, try again.',
	requiredError    : 'Required! Try again.',
	invalidError     : 'Invalid input: ',
	attemptsError    : 'Maximum attempts reached!',
	stdin            : null,
	stdout           : null,
	stderr           : null,
	timeout          : null,
	confirm          : false,
	overrideDefaults : {}
};

// Provides chalk
Prompt.chalk = chalk;

// Helpers for boolean questions
Prompt.isBool = /^(?:y(?:es)?|n(?:o)?)$/i;
Prompt.filterBool = function(value) {
	value = value.toLowerCase();
	if (value === 'y' || value === 'yes') return true;
	return false;
};

// Ask a question
Prompt.prototype.ask = function(question, options, callback) {

	// Check callback
	if (typeof callback !== 'function') {
		callback = options;
		options = undefined;
	}

	// Options are optional
	if (typeof options === 'undefined') {
		options = {};
	}

	// ask multiple questions
	if (question instanceof Array) {
		askMultiple.call(this, question, options, callback);
		return;
	}

	// Can pass question in options
	if (typeof question === 'object') {
		options = question;
		question = options.question;
	}

	askSingle.call(this, question, options, callback);

};

// Ask multiple questions
function askMultiple(questions, options, callback) {

	var output = {},
		errors = null,
		index = 0,
		len = questions.length,
		me = this;

	// On completion of prompts
	function finished() {
		if (options.confirm) {

			// Display before confirmation
			if (options.confirm.before) {
				log.call(me, options.confirm.before);
			};

			// Display input
			for (var i in questions) {
				if (!options.confirm.all) {
					// Only display prompts that were asked
					switch (typeof questions[i].depends) {
						case 'boolean':
							if (!questions[i].depends) continue;
							break;
						case 'function':
							if (!questions[i].depends(output)) continue;
							break;
					}
				}

				var key = questions[i].key || questions[i].question;
				logConfirmation.call(me, questions[i].question, output[key]);
			}

			// Display after confirmation
			if (options.confirm.after) {
				log.call(me, options.confirm.after);
			}

			// Ask for confirmation
			me.ask(options.confirm.message || 'Confirm your input (Y/n)', {
				default: options.confirm.default || 'Y',
				boolean: true
			}, function(err, res) {
				if (res) {
					callback(errors, output);
				} else {
					return askMultiple.call(me, questions, options, callback);
				}
			});
		} else {
			callback(errors, output);
		}
	}

	// Loop through prompts
	var next = function(err, res) {
		// The key is either specified or just the question
		var key = questions[index].key || questions[index].question;

		// Keep the errors
		if (err != null) {
			if (errors === null) errors = {};
			errors[key] = err;
		}

		// Keep the output
		if (res != null) output[key] = res;

		// If end of questions, callback
		if (index == len-1) {
			finished();
			return;
		}

		// Increment and next
		++index;
		askSingle.call(me, questions[index].question, extend({}, options, questions[index]), next, output);
	};

	// Start the loop
	askSingle.call(this, questions[index].question, extend({}, options, questions[index]), next, output);
}

// Ask a single question
function askSingle(question, options, callback, _output) {

	// Question and callback are not!
	if (typeof question !== 'string' || typeof callback !== 'function')
		throw new TypeError('Both question and callback are required!');

	// Merge options
	options = extend({}, this.options, options);

	// Set the key to the question if it doesn't exist
	if (!options.key)
		options.key = question;

	// Set default override
	if (options.overrideDefaults && typeof options.overrideDefaults[options.key] !== 'undefined') {
		var def = options.overrideDefaults[options.key];
		if (options.boolean) {
			if (options.overrideDefaults[options.key]) {
				def = 'Y';
			} else {
				def = 'N';
			}
		}
		options.default = def;
	}
	

	// Prompt depends
	switch (typeof options.depends) {
		case 'boolean':
			if (!options.depends) {
				return callback(null, doAfterFilters(options.default, options));
			}
			break;
		case 'function':
			if (!options.depends(_output)) {
				return callback(null, doAfterFilters(options.default, options));
			}
			break;
	}

	// Build prompt string
	question = promptText(question, options);

	// Ask the question
	askQuestion.call(this, question, options, callback);

};

// Builds the prompt string
function promptText(text, options) {
	if (options.prefix) {
		options.prefix = options.prefixTheme(options.prefix);
	}
	text = options.textTheme(text);
	if (options.default) {
		var def = options.defaultTheme(options.defaultPrefix + options.default + options.defaultSuffix);
	}
	if (options.suffix) {
		options.suffix = options.suffixTheme(options.suffix);
	}

	return options.prefix + text + (def || '') + options.suffix;
};

// Just displays a prompt
function displayPrompt(text, callback) {
	read({
		prompt: text,
		input: this.options.stdin || process.stdin,
		output: this.options.stdout || process.stdout,
		terminal: false,
		timeout: this.options.timeout
	}, callback.bind(this));
};

// The actuall asking
function askQuestion(question, options, callback, _attempt) {
	if (!_attempt) _attempt = 0;
	_attempt++;

	if (options.attempts && _attempt > options.attempts) {
		logError.call(this, options.attemptsError);
		return callback(options.attemptsError, '');
	}

	displayPrompt.call(this, question, function(err, res) {

		if (err) {
			if (err.message == 'canceled')
				return process.exit(err);
			if (_attempt > 2)
				return callback(err+'', '');
			logError.call(this, options.inputError);
			return askQuestion.call(this, question, options, callback, _attempt);
		}

		// Before filter
		if (typeof options.before === 'function') {
			res = options.before(res);
		}

		// If default, assign it if empty
		if (typeof options.default !== 'undefined' && res == '') {
			res = options.default;
		}

		// Required?
		if (options.required && (typeof res === 'undefined' || res == '' || !res)) {
			logError.call(this, options.requiredError);
			return askQuestion.call(this, question, options, callback, _attempt);
		}

		// Do boolean check
		if (options.boolean) {
			if (!Prompt.isBool.test(res)) {
				logError.call(this, options.invalidError + res);
				return askQuestion.call(this, question, options, callback, _attempt);
			}
		}

		// Custom validation function
		if (typeof options.validate === 'function') {
			if (!options.validate(res)) {
				logError.call(this, options.invalidError + res);
				return askQuestion.call(this, question, options, callback, _attempt);
			}
		} else if (options.validate instanceof RegExp) {
			if (!options.validate.test(res)) {
				logError.call(this, options.invalidError + res);
				return askQuestion.call(this, question, options, callback, _attempt);
			}
		}

		res = doAfterFilters(res, options);

		return callback(null, res);
	});
};

// Do the after filters
function doAfterFilters(res, options) {
	// After filter
	if (typeof options.after === 'function') {
		res = options.after(res);
	}
	// Do boolean filter
	if (options.boolean) {
		res = Prompt.filterBool(res);
	}
	return res;
};

// Standard error log format
function logError(msg) {
	if (this.options.stderr) {
		this.options.stderr.write(chalk.red(msg));
	} else {
		console.error(chalk.red(msg));
	}
};

// Standard confirmation log format
function logConfirmation(key, val) {
	var keyTheme = this.options.confirm.keyTheme || chalk.bold.grey;
	var valTheme = this.options.confirm.valTheme || chalk.cyan;
	var suffix = this.options.confirm.suffix || ': ';
	switch (typeof val) {
		case 'undefined': return;
		case 'object': if(val === null) return;
		case 'boolean': (val) ? val = 'Yes' : val = 'No'; break;
	}
	log.call(this, keyTheme(key + suffix) + valTheme(val));
};

// Log to console or stdout
function log(out) {
	if (this.options.stdout) {
		this.options.stdout.write(out);
	} else {
		console.log(out);
	}
};

// Export prompt
module.exports = Prompt;
