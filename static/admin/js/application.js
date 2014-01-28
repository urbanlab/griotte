

$( document ).bind( "pageinit", function( event ) {
  $('#toggle-scenario').bind('slidestop', function() {
    Application.scenario($('#toggle-scenario').prop('value'));
  });

  $('#toggle-sound').bind('slidestop', function() {
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
    Application.started = Math.floor(Date.now() / 100);
    Application.graph = {};
    Application.sensor_data = { 'an0': [], 'an1': [], 'an2': [], 'an3': [],
                                'io0': [], 'io1': [], 'io2': [], 'io3': [] };

    Application.sliderprogress = $('#slider-current');
    Application.slidersound    = $('#slider-sound');
    Application.togglesound    = $('#toggle-sound');
    Application.togglescenario = $('#toggle-scenario');

    Application.media_duration = $('#media-duration');
    Application.media_name     = $('#media-name');

    Application.prefix = location.hostname.split('.')[0];

    Application.graph_range = 10000;

    Application.graph_options = {};

    Application.graph_options['an'] = {
      yaxis: {
        max: 5.5,
        min: -0.5,
      },
      xaxis : {
        title: 'Analog',
        mode: 'time',
        timeUnit: 'millisecond',
      },
    };

    Application.graph_options['io'] = {
      yaxis: {
        max: 1.5,
        min: -0.5,
        ticks: [[0,"Low"],[1,"High"]],
      },
      xaxis: {
        title: 'Digital',
        mode: 'time',
        timeUnit: 'millisecond',
      },
    };

    $('#radio-1sec').click(function() {
      Application.graph_range = 1000;
    });
    $('#radio-10secs').click(function() {
      Application.graph_range = 10000;
    });
    $('#radio-1min').click(function() {
      Application.graph_range = 60000;
    });
    $('#radio-10mins').click(function() {
      Application.graph_range = 600000;
    });

    console.log("Application initialized");

    Griotte.subscribe('internal.ready', Application.launch);
  },

  launch: function() {
    console.log("Application.launch called");
    Griotte.subscribe("store.set.sound_level", Application.sound_in);
    Griotte.subscribe("video.event.status", Application.video_in);
    Griotte.subscribe("video.event.stop", Application.video_in);
    Griotte.subscribe("analog.event.an0.sample", Application.sensor_in);
    Griotte.subscribe("analog.event.an1.sample", Application.sensor_in);
    Griotte.subscribe("analog.event.an2.sample", Application.sensor_in);
    Griotte.subscribe("analog.event.an3.sample", Application.sensor_in);
    Griotte.subscribe("digital.event.io0.edge.rising", Application.sensor_in);
    Griotte.subscribe("digital.event.io1.edge.rising", Application.sensor_in);
    Griotte.subscribe("digital.event.io2.edge.rising", Application.sensor_in);
    Griotte.subscribe("digital.event.io3.edge.rising", Application.sensor_in);
    Griotte.subscribe("digital.event.io0.edge.falling", Application.sensor_in);
    Griotte.subscribe("digital.event.io1.edge.falling", Application.sensor_in);
    Griotte.subscribe("digital.event.io2.edge.falling", Application.sensor_in);
    Griotte.subscribe("digital.event.io3.edge.falling", Application.sensor_in);

    for (var i = 0; i < 4; i++) {
      Griotte.publish("analog.command.an" + i + ".periodic_sample", { every: 0.1 } );
    };
  },

  scenario: function(state) {
    Griotte.publish('.' + Application.prefix + '.scenario', { command: state });
  },

  sound: function(state, volume) {
    Griotte.publish("store.set.sound_level", { state: state, level: parseInt(volume) } );
  },

  sensor_in: function(message) {
    var chan = message.channel.split('.')[2],
        container,
        index = Date.now(); // - Application.started

    // Dirty trick ahead :
    if (chan[0] == 'a') {
      /* To have flat digital graphs, we'll fill-in values for io here, even if
      we had no incoming value. the fact is digital doesn't support
      periodic_sampling for now so we'll just fake it this way */
      for (var i = 0; i < 4; i++) {
        var lastval_index = Application.sensor_data['io' + i].length
        if (lastval_index > 1) {
          var lastval = Application.sensor_data['io' + i][lastval_index-1][1];
          Application.sensor_data['io' + i].push([ index, lastval ]);
        }
      }
    }

    Application.sensor_data[chan].push([ index, message.data.raw_value ])

    var style = ['an','io'];
    var data = {'an': [], 'io': []};

    for (var s = style.length - 1; s >= 0; s--) {
      var data = [];

      // Come on, make a damn loop !
      container = document.getElementById("graph-" + style[s] + "-container");
      for (var ch = 0; ch < 4; ch++) {
        // We redraw both, for io-periodic sample hack effect
        data.push({ data: Application.sensor_data[style[s] + ch], label: style[s] + ch })
      }

      Application.graph_options[style[s]]['xaxis']['min'] = Math.max(Application.started, index - Application.graph_range);
      Application.graph_options[style[s]]['xaxis']['max'] = index;

      Application.graph[style[s]] = Flotr.draw(container,
                                               data,
                                               Application.graph_options[style[s]]);
    };
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
      console.log("data.media is " + data.media);
      Application.media_name.text(data.media);
      Application.sliderprogress.prop({ value: Math.floor(data.position/1000) });
      Application.sliderprogress.prop({ max: Math.floor(data.duration/1000) });
    } else if (message.channel == 'video.event.play') {
      Application.media_duration.text(data.duration/1000);
      Application.media_name.text(data.media);
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
