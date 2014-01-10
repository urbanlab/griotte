

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

  init: function() {
    Application.sliderprogress = $('#slider-current');
    Application.slidersound    = $('#slider-sound');
    Application.togglesound    = $('#toggle-sound');
    Application.togglescenario = $('#toggle-scenario');

    Application.media_duration = $('#media-duration');
    Application.media_name     = $('#media-name');

    Application.prefix = location.hostname.split('.')[0];

    console.log("Application initialized");

    Griotte.subscribe('internal.ready', Application.launch);
  },

  launch: function() {
    console.log("Application.launch called");
    Griotte.subscribe("store.set.sound_level", Application.sound_in);
    Griotte.subscribe("video.event.status", Application.video_in);
    Griotte.subscribe("video.event.stop", Application.video_in);
  },

  scenario: function(state) {
    Griotte.publish('.' + Application.prefix + '.scenario', { command: state });
  },

  sound: function(state, volume) {
    Griotte.publish("store.set.sound_level", { state: state, level: parseInt(volume) } );
  },

  scenario_in: function(data) {
    console.log("scenario event in");
    console.log(data);
    Application.togglescenario.prop({ value: data['command'] });
    Application.togglescenario.slider('refresh');
  },

  video_in: function(message) {
    data = message.data
    console.log("video event in");
    console.log(data);
    if (message.channel == 'video.event.status') {
      Application.media_duration.text(data.duration/1000);
      Application.media_name.text(data.media_name);
      Application.sliderprogress.prop({ value: Math.floor(data.position/1000) });
      Application.sliderprogress.prop({ max: Math.floor(data.duration/1000) });
    } else if (message.channel == 'video.event.play') {
      Application.media_duration.text(data.duration/1000);
      Application.media_name.text(data.media_name);
      Application.sliderprogress.prop({ max: data.duration });
    } else if (message.channel == 'video.event.stop') {
      Application.media_name.text('Aucun');
      Application.media_duration.text('N/A');
      Application.sliderprogress.prop({ value: Math.floor(data.duration/1000) });
    }

    Application.sliderprogress.slider('refresh');
  },


  sound_in: function(message) {
    data = message.data
    console.log("sound event in");
    console.log(data);

    // Toggle
    console.log(Application.togglesound);
  //    Application.togglesound.slider({ value: data['state'] });
    Application.togglesound.prop({ value: data.state });
    Application.togglesound.slider('refresh');

    console.log(Application.slidersound);
    if (data['state'] == 'off') {
      Application.slidersound.slider('disable');
    } else {
      Application.slidersound.slider('enable');
    }

    // Slider
    console.log("setting value prop for slider to " + data.level);
    Application.slidersound.prop({ value: data['level'] });
    Application.slidersound.slider('refresh');
  },
};
