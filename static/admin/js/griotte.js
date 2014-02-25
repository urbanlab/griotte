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
      self._events[message.channel](message);
    }
  },

  subscribe: function(channel, callback) {
    var self = this;

    self._events[channel] = callback;
    //console.log("subscribing to " + channel);

    if (channel == ".internal.ready" && self.ready) {
      self.dispatch({"channel": "internal.ready"});
    }

    self.publish("meta.subscribe", { channel: channel });
  },

  unsubscribe: function(channel) {
    var self = this;

    delete self._events[channel];
    // console.log("unsubscribing from " + channel);

    self.publish("meta.subscribe", { channel: channel });
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



