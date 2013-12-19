

$( document ).bind( "pageinit", function( event ) {
  $('#toggle-scenario').bind('slidestop', function() {
    Application.scenario($('#toggle-scenario').prop('value'));
  });

  $('#toggle-sound').bind('slidestop', function() {
/*    console.log($('#toggle-sound'));
    if ($('#toggle-sound').prop('value') == 'off') {
      $('#slider-sound').slider('disable');
    } else {
      $('#slider-sound').slider('enable');
    };*/
    Application.sound($('#toggle-sound').prop('value'), $('#slider-sound').prop('value'));
  });

  $('#slider-sound').bind('slidestop', function() {
    console.log($('#slider-sound'));
    Application.sound($('#toggle-sound').prop('value'), $('#slider-sound').prop('value'));
  });
});


Application = {
  /**
   * Initializes the application, passing in the globally shared griotte client.
   * Apps on the same page should share a griotte client so that they may share
   * an open HTTP connection with the server.
   */

  init: function(griotte) {
    var self = this;
    this._griotte = griotte;

    console.log("griotte state : " + griotte.ready);

    this._heartbeat  = $('#heartbeat');
    this._heartbeat.hide();

    this._sliderprogress = $('#slider-current');
    this._slidersound = $('#slider-sound');
    this._togglesound = $('#toggle-sound');
    this._togglescenario = $('#toggle-scenario');

    this._prefix = location.hostname.split('.')[0];

    console.log("Application initialized");

    this._griotte.subscribe('internal.ready', self.launch.bind(this));
  },

  launch: function() {
    console.log("Application.launch called");
    console.log(self)
    this._griotte.subscribe("meta.store.sound_level.set", this.sound_in.bind(this));
    this._griotte.subscribe("message.video", this.video_in.bind(this));

  },

  accept: function(message) {
    this._heartbeat.fadeIn(500, function() { $(this).fadeOut(500); } );
  },

  scenario: function(state) {
    this._griotte.publish('.' + this._prefix + '.scenario', { command: state });
  },

  sound: function(state, volume) {
    this._griotte.publish("meta.store.sound_level.set", { state: state, level: parseInt(volume) } );
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

  video_in: function(message) {
    data = message.data
    console.log("video event in");
    console.log(data);
    if (data['type'] == 'status') {
      this._sliderprogress.prop({ value: Math.floor(data.position/1000) });
      this._sliderprogress.prop({ max: Math.floor(data.media_length/1000) });
    } else if (data['type'] == 'play') {
      this._sliderprogress.prop({ max: data.media_length });
    } else if (data['type'] == 'stop') {
      this._sliderprogress.prop({ value: Math.floor(data.media_length/1000) });
    }
    this._sliderprogress.slider('refresh');
  },


  sound_in: function(message) {
    data = message.data
    console.log("sound event in");
    console.log(data);

    // Toggle
    console.log(this._togglesound);
  //    this._togglesound.slider({ value: data['state'] });
    this._togglesound.prop({ value: data.state });
    this._togglesound.slider('refresh');

    console.log(this._slidersound);
    if (data['state'] == 'off') {
      this._slidersound.slider('disable');
    } else {
      this._slidersound.slider('enable');
    }

    // Slider
    console.log("setting value prop for slider to " + data.level);
    this._slidersound.prop({ value: data['level'] });
    this._slidersound.slider('refresh');
  },
};
