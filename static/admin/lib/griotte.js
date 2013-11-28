
$( document ).bind( "pageinit", function( event ) {
  $('#toggle-scenario').bind('slidestop', function() {
    Raspberry.scenario($('#toggle-scenario').prop('value'));
  });

  $('#toggle-sound').bind('slidestop', function() {
/*    console.log($('#toggle-sound'));
    if ($('#toggle-sound').prop('value') == 'off') {
      $('#slider-sound').slider('disable');
    } else {
      $('#slider-sound').slider('enable');
    };*/
    Raspberry.sound($('#toggle-sound').prop('value'), $('#slider-sound').prop('value'));
  });

  $('#slider-sound').bind('slidestop', function() {
    console.log($('#slider-sound'));
    Raspberry.sound($('#toggle-sound').prop('value'), $('#slider-sound').prop('value'));
  });
});



Logger = {
  incoming: function(message, callback) {
    console.log('incoming', message);
    callback(message);
  },
  outgoing: function(message, callback) {
    console.log('outgoing', message);
    callback(message);
  }
};


Griotte = {
  init: function(url) {
    var self = this;

    this._url = url
    this._ws = new WebSocket(url);
    this._callbacks = new Array()

    this._ws.onopen = function() {
      self._ws.send("Websocket connected to " + url);
      self.ready = true;
    };

    this._ws.onmessage = function(message) {
      console.log(message.data);
      for (var i = 0; i < self._callbacks.length; i++) {
        console.log("calling cb");
        self._callbacks[i];
        //Do something
      }
    };

    this._ws.onclose = function() {
      console.log("Websocket closed");
      self.ready = false;
    }
    return this;
  },
  subscribe: function(channel, callback) {
    var self = this;

    self._callbacks.push(callback);
    console.log("subscribing to " + channel);
    var msg = { "type":"subscribe", "channel":channel};
    self.publish(channel, JSON.stringify({ "type":"subscribe" }));
  },
  publish: function(channel, data) {
    var self = this;
    var channel = '_' + channel

    console.log("publishing " + data + " to " + channel);
    var msg = { "channel":channel, "data":data};
    self._ws.send(JSON.stringify(msg));
  },
  ready: function() {
    return this.ready;
  }
}

Raspberry = {
  /**
   * Initializes the application, passing in the globally shared Bayeux client.
   * Apps on the same page should share a Bayeux client so that they may share
   * an open HTTP connection with the server.
   */
  init: function(bayeux) {
    var self = this;
    this._bayeux = bayeux;

    console.log("Bayeux state : " + bayeux.ready);
   // while (!bayeux.ready) {
    //  console.log(".");
    //};

    this._heartbeat  = $('#heartbeat');
    this._heartbeat.hide();

    this._slidersound = $('#slider-sound');
    this._togglesound = $('#toggle-sound');
    this._togglescenario = $('#toggle-scenario');

    this._prefix = location.hostname.split('.')[0];

    console.log("Raspberry initialized");
  },

  /**
   * Starts the application after a username has been entered. A subscription is
   * made to receive messages that mention this user, and forms are set up to
   * accept new followers and send messages.
   */
  launch: function() {
    var self = this;
    //this._bayeux.subscribe('/' + this._prefix + '/heartbeats', this.accept, this);
    this._bayeux.subscribe('/heartbeats', this.accept, this);
    this._bayeux.subscribe('/' + this._prefix + '/sound', this.sound_in, this);
    this._bayeux.subscribe('/' + this._prefix + '/scenario', this.scenario_in, this);

    this._bayeux.publish('/', 'hello');
    // Detect network problems and disable the form when offline
/*    this._bayeux.bind('transport:down', function() {
      console.log("Transport is down");
      $('#transport').html('(down)');

    }, this);
    this._bayeux.bind('transport:up', function() {
      console.log("Transport is up");
    }, this);
    */
  },

  /**
   * Handler for messages received over subscribed channels. Takes the message
   * object sent by the post() method and displays it in the user's message list.
   */
  accept: function(message) {
    this._heartbeat.fadeIn(500, function() { $(this).fadeOut(500); } );
  },

  scenario: function(state) {
    this._bayeux.publish('/' + this._prefix + '/scenario', {command: state});
  },

  sound: function(state, volume) {
    this._bayeux.publish('/' + this._prefix + '/sound', {state: state, level: parseInt(volume)});
  },

  scenario_in: function(data) {
    console.log("scenario event in");
    console.log(data);

    // Toggle
//    console.log(this._togglesound);
//    this._togglesound.slider({ value: data['state'] });
/*    if (data['state'] == 'play') {
      state = 'on';
    } else {
      state = 'off'
    }
*/
    this._togglescenario.prop({ value: data['command'] });
    this._togglescenario.slider('refresh');
  },

/*  scenario_in: function(data) {
    console.log("scenario event in");
    console.log(data);

    // Toggle
//    console.log(this._togglesound);
//    this._togglesound.slider({ value: data['state'] });
    if (data['state'] == 'play') {
      state = 'on';
    } else {
      state = 'off'
    }

    this._togglescenario.prop({ value: state });
    this._togglescenario.slider('refresh');
  },
*/
  sound_in: function(data) {
    console.log("sound event in");
    console.log(data);

    // Toggle
    console.log(this._togglesound);
//    this._togglesound.slider({ value: data['state'] });
    this._togglesound.prop({ value: data['state'] });
    this._togglesound.slider('refresh');

    if (data['state'] == 'off') {
      this._slidersound.slider('disable');
    } else {
      this._slidersound.slider('enable');
    }

    // Slider
    this._slidersound.prop({ value: data['level'] });
    this._slidersound.slider('refresh');
  }
};
