Griotte = {
  init: function(url) {
    var self = this;

    this._url = url
    this._ws = new WebSocket(url);
    this._events = {};
    this.ready = false;

    self._ws.onopen = function() {
      console.log("Websocket connected");
      self.ready = true;
      self.dispatch({"channel": "internal.ready"});
    };

    self._ws.onmessage = function(message) {
      data = JSON.parse(message.data)
      self.dispatch(data);
    };

    self._ws.onclose = function() {
      console.log("Websocket closed");
      self.ready = false;
    };

    console.log("Griotte initialized");
  },

  dispatch: function(message) {
    var self = this;

    if (self._events.hasOwnProperty(message.channel)) {
      for (index = 0; index < self._events[message.channel].length; ++index) {
       self._events[message.channel][index](message);
      }
    }
  },

  subscribe: function(channel, callback) {
    var self = this;

    if (! self._events.hasOwnProperty(channel)) {
      self._events[channel] = [];
    }

    self._events[channel].push(callback);
    //console.log("subscribing to " + channel);

    if (channel == ".internal.ready" && self.ready) {
      self.dispatch({"channel": "internal.ready"});
    }

    self.publish("meta.subscribe", { channel: channel });
  },

  unsubscribe: function(channel, callback) {
    var self = this;

    var index = self._events[channel].indexOf(callback);
    if (index > -1) {
      self._events[channel].splice(index, 1);
    }
    // console.log("unsubscribing from " + channel);

    self.publish("meta.unsubscribe", { channel: channel });
  },

  publish: function(channel, data) {
    var self = this;
    if (self.ready) {
      // console.log("publishing " + JSON.stringify(data) + " to " + channel);
      var msg = { channel: channel, data: data };
      self._ws.send(JSON.stringify(msg));
    } else {
      console.log("Websocket not ready, dropping message");
    }

  },
};



