$(document).bind('pageinit', 
    function(){
      $('#mute').change('click', 
        function(e) {
          console.log("clicked" + $('#volume').val() + " mute is " + $('#mute').val());
          Raspberry.sound($('#mute').val(), $('#volume').val());
          if ($('#mute').val() == 'on') {
            $('#volume').slider('enable');
            $('#volume').textinput('enable');
          } else {
            $('#volume').slider('disable');
            $('#volume').textinput('disable');
          };
        });
      $('#volume').on('slidestop',
        function(e) {
          console.log("stopped");
          Raspberry.sound($('#mute').val(), $('#volume').val());
        });
});
