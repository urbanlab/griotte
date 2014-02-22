$( document ).ready(function( event ) {

  $('#upload-form').on('submit', function() {
    var formData = new FormData($(this)[0]);

    console.log($(this)[0]);

    if ($('#filearg').val() == "") {
      $('#popup-title').text("Don't be stupid");
      $('#popup-content').text("You need to select a file first !");
      $.mobile.changePage('#page-popup', {
        transition : 'pop',
      });        return false;
    }

    $.ajax({
        url:"/upload",
        type:"POST",
        data:formData,
        contentType:false,
        processData:false,
        cache:false,
        success:function(resp){
            $('#upload-progress').attr({value:0})
            $('#upload-progress').slider("refresh");
            $('#upload-slider-container').fadeOut(500);
            //$('#upload-progress').parent().find('.ui-slider-track').fadeOut(500);
        },
        error:function(resp){
            $('#upload-progress').prop({value:0});
            //$('#upload-progress').slider('disable');

            $('#popup-title').text("Unable to upload file");
            $('#popup-content').text("Sorry, I couldn't upload the file because I had this error :" + resp.statusText);
            $.mobile.changePage('#page-popup', {
              transition : 'pop',
            });
        },
        xhr:function(){
            myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){
  //              $('#upload-progress').parent().find('.ui-slider-track').fadeIn(500);
                $('#upload-slider-container').fadeIn(500);
                myXhr.upload.addEventListener('progress', Application.upload_progress,false);
            }
            return myXhr;
        }
    });
    return false;
  });
});

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


  $('.custom-collapsible').bind('collapsibleexpand', function(event) {
    var type = $(this).attr("id").split('-')[0];
    console.log(type + ' collapsible expanded');
    $.ajax({
      url:'/api/' + type,
      type:"GET",
      contentType:false,
      processData:false,
      cache:false,
      dataType: 'json',
      success:function(resp) {
        console.log(resp)
        $("#" + type + "-list").empty();
        console.log('got ' + resp.length + ' elements');
        var code = "";
        $.each(resp, function(index, element) {
          console.log("adding " + element.name);
          code += '<li class="ui-li-has-thumb ui-first-child">';
          code += '<a href="#" class="ui-btn ui-btn-icon-right ui-icon-carat-r">\n<img src="' + element.thumbnail + '" />\n';
          code += '<h3>' + element.name + '</h3>';

          $.each(['description', 'duration', 'codec'], function(index, key) {
            console.log(key + "=>" + element[key]);
            if (element[key]) {
              keycap = key[0].toUpperCase() + key.slice(1); // capitalize... thanks JS
              code = code + '<p><strong> ' + keycap + '</strong> : ' +  element[key] + '</p>';
            };
          });
          if (type == 'scenario') {
            code += '<button type="button" data-inline="true" data-mini="true" data-role="button" data-icon="edit">Edit</button>';
            code += '<button type="button" data-inline="true" data-mini="true" data-role="button" data-icon="run">Run</button>';
            code += '<div data-role="fieldcontain"> \
              <label for="toggle-sound">Son</label> \
              <select name="toggle-sound" id="toggle-sound" data-role="slider" data-mini="true"> \
                <option value="off">Off</option> \
                <option value="on">On</option> \
              </select> \
            </div>';
          } else {
            code += '<button type="button" data-inline="true" data-mini="true" data-role="button" data-icon="delete">Play</button>';
          }
          code += '<button type="button" data-inline="true" data-mini="true" data-role="button" data-icon="delete">Delete</button>';
          code += '</a></li>';
        });
        console.log("adding code " + code);
        $('#' + type + '-list').html(code);
      },
    });
  });

  $('#upload-progress').css('margin-left','-9999px'); // Fix for some FF versions
  $('#upload-progress').find('.ui-slider-track').css('margin','0 15px 0 15px');
  $('#upload-progress').parent().find('.ui-slider-handle').hide();
  $('#upload-slider-container').hide();
});

Application = {
  /**
   * Initializes the application, passing in the globally shared griotte client.
   * Apps on the same page should share a griotte client so that they may share
   * an open HTTP connection with the server.
   */

  init: function() {
    Application.started = Date.now();
    Application.graph = {};
    Application.sensor_data = { 'an0': [], 'an1': [], 'an2': [], 'an3': [],
                                'io0': [[Application.started,0]], 'io1': [[Application.started,0]], 'io2': [[Application.started,0]], 'io3': [[Application.started,0]] };

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
    console.log("Application initialized");

    setInterval(Application.normalize_digital_data, 200);
    setInterval(Application.trim_data, 5000);

    Griotte.subscribe('internal.ready', Application.launch);
  },

  launch: function() {
    console.log("Application.launch called");
    Griotte.subscribe("store.command.set.sound_level", Application.sound_in);
    Griotte.subscribe("store.event.sound_level", Application.sound_in);
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
    Griotte.subscribe("store.event.medias", Blockly.Medias.callbackMedias);

    for (var i = 0; i < 4; i++) {
      Griotte.publish("analog.command.an" + i + ".periodic_sample", { every: 2.0 } );
    };

    // Get initial sound settings
    Griotte.publish("store.command.get.sound_level", {});

    // Get initial medias
    Griotte.publish("store.command.get.medias", {});
  },

  upload_progress: function(evnt){
    if(evnt.lengthComputable){
      var ratio = (evnt.loaded / evnt.total) * 100;
      console.log("setting val to " + ratio);
      $('#upload-progress').val(ratio);
      $('#upload-progress').slider('refresh');
    }
  },

  scenario: function(state) {
    Griotte.publish('.' + Application.prefix + '.scenario', { command: state });
  },

  sound: function(state, volume) {
    Griotte.publish("store.command.set.sound_level", { value: { state: state, level: parseInt(volume) } } );
  },

  normalize_digital_data: function() {
    var index = Date.now();
    for (var ch = 0; ch < 4; ch++) {
      if (Application.sensor_data["io" + ch].length > 0) {
        var lastval = Application.sensor_data["io" + ch][Application.sensor_data["io" + ch].length - 1][1];
        Application.sensor_data["io" + ch].push([index, lastval]);
      }
    }
  },

  // Poor man's garbage collector
  trim_data: function() {
    var index = Date.now();
    for (var key in dat = Object.keys(Application.sensor_data)) {
      while (Application.sensor_data[dat[key]].length > 0 && Application.sensor_data[dat[key]][0][0] <
             (index - 60000)) {
         Application.sensor_data[dat[key]].shift();
      }
    }
  },

  sensor_in: function(message) {
    var chan = message.channel.split('.')[2],
        container,
        index = Date.now(), // - Application.started
        style = ['an','io'],
        data = [];

    Application.sensor_data[chan].push([ index, message.data.raw_value ])

    for (var s = style.length - 1; s >= 0; s--) {
      data = [];
      //container = document.getElementById("graph-" + style[s] + "-container");
      container = $("#graph-" + style[s] + "-container")
      if (! container.is(":visible")) {
        return;
      }
      for (var ch = 0; ch < 4; ch++) {
        data.push({ data: Application.sensor_data[style[s] + ch], label: style[s] + ch })
      }

      Application.graph_options[style[s]]['xaxis']['min'] = Math.max(Application.started, index - Application.graph_range);
      Application.graph_options[style[s]]['xaxis']['max'] = index;

      Application.graph[style[s]] = Flotr.draw(container.get(0),
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
    data = message.data.value

    Application.togglesound.prop({ value: data.state });
    Application.togglesound.slider('refresh');

    if (data['state'] == 'off') {
      Application.slidersound.slider('disable');
    } else {
      Application.slidersound.slider('enable');
    }

    // Slider
    Application.slidersound.prop({ value: data['level'] });
    Application.slidersound.slider('refresh');
  },
};
