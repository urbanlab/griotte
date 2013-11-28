$( document ).bind( "pageinit", function() {
  // setup some defaults for jsPlumb. 
  jsPlumb.importDefaults({
    Endpoint : ["Dot", {radius:2}],
    HoverPaintStyle : {strokeStyle:"#1e8151", lineWidth:2 },
    ConnectionOverlays : [
      [ "Arrow", { 
        location:1,
        id:"arrow",
        length:14,
        foldback:0.8
      } ],
      [ "Label", { label:"FOO", id:"label", cssClass:"aLabel" }]
    ]
  });
      
  var windows = $(".w");
  // initialise draggable elements.  
  jsPlumb.draggable(windows);

  // bind a click listener to each connection; the connection is deleted. you could of course
  // just do this: jsPlumb.bind("click", jsPlumb.detach), but I wanted to make it clear what was
  // happening.
  jsPlumb.bind("click", function(c) { 
    jsPlumb.detach(c); 
  });     

  // make each ".ep" div a source and give it some parameters to work with.  here we tell it
  // to use a Continuous anchor and the StateMachine connectors, and also we give it the
  // connector's paint style.  note that in this demo the strokeStyle is dynamically generated,
  // which prevents us from just setting a jsPlumb.Defaults.PaintStyle.  but that is what i
  // would recommend you do. Note also here that we use the 'filter' option to tell jsPlumb
  // which parts of the element should actually respond to a drag start.
  jsPlumb.makeSource(windows, {
    filter:".ep",       // only supported by jquery
    anchor:"Continuous",
    connector:[ "StateMachine", { curviness:20 } ],
    connectorStyle:{ strokeStyle:"#5c96bc", lineWidth:2, outlineColor:"transparent", outlineWidth:4 },
    maxConnections:5,
    onMaxConnections:function(info, e) {
      alert("Maximum connections (" + info.maxConnections + ") reached");
    }
  });     

  // bind a connection listener. note that the parameter passed to this function contains more than
  // just the new connection - see the documentation for a full list of what is included in 'info'.
  // this listener sets the connection's internal
  // id as the label overlay's text.
  jsPlumb.bind("connection", function(info) {
    info.connection.getOverlay("label").setLabel(info.connection.id);
  });

  // initialise all '.w' elements as connection targets.
  console.log($(".w"));
  jsPlumb.makeTarget(windows, {
    dropOptions:{ hoverClass:"dragHover" },
    anchor:"Continuous"       
  });
      
  // and finally, make a couple of connections
  //jsPlumb.connect({ 
  //  source:"start-0", 
  //  target:"analog0-0",
  //  overlays: [[ "Label", { label:"gooo", id:"label", cssClass:"aLabel" }]]
  //});

  //jsPlumb.connect({ source:"analog0-0", target:"video-0", overlays: [[ "Label", { label:"distance < 100 cm", id:"label", cssClass:"aLabel" }]] });            
 
//          <div class="w" id="start-0">Départ<div class="ep"></div></div>
//          <div class="w" id="start-1">Départ<div class="ep"></div></div>
//          <div class="w" id="start-2">Départ<div class="ep"></div></div>
//          <div class="w" id="analog0-0">Capteur AN0<div class="ep"></div></div>
//          <div class="w" id="video-0">Lecture vidéo<div class="ep"></div></div>
//          <div class="w" id="sound-0">Lecture son<div class="ep"></div></div>
//          <div class="w" id="image-0">Lecture son<div class="ep"></div></div>
//          <div class="w" id="pause-0">Pause<div class="ep"></div></div>
//          <div class="w" id="io-0">Capteur IO0<div class="ep"></div></div> 
//          <div class="w" id="io-1">Capteur IO1<div class="ep"></div></div> 
//          <div class="w" id="time-1">Heure<div class="ep"></div></div> 

});

