$(document).bind('pageinit', function() {
  $( "#scenario-elements" ).sortable({ items: "li:not(.ui-state-disabled)" });
  // $( "#scenario-elements" ).sortable();
  $( "#scenario-elements" ).disableSelection();
  <!-- Refresh list to the end of sort to have a correct display -->
  $( "#scenario-elements" ).bind( "sortstop", function(event, ui) {
    $('#scenario-elements').listview('refresh');
  });

  $( ".mediaitem" ).on("click", function() {
    h = $(this).parent("a").get()
    console.log(h);
    $( "#scenario-elements" ).add($(this).parent("a").get());
  });

  // Swipe to remove list item
  $( document ).on( "swipeleft swiperight", "#scenario-elements li.ui-li", function( event ) {
    var listitem = $( this ),
    // These are the classnames used for the CSS transition
    dir = event.type === "swipeleft" ? "left" : "right",
    // Check if the browser supports the transform (3D) CSS transition
    transition = $.support.cssTransform3d ? dir : false;
    listitem.remove();
    $( "#scenario-elements" ).listview( "refresh" );
    //confirmAndDelete( listitem, transition );
  });

  // If it's not a touch device...
  if ( ! $.mobile.support.touch ) {

    // Remove the class that is used to hide the delete button on touch devices       
    $( "#scenario-elements" ).removeClass( "touch" );

    // Click delete split-button to remove list item
    $( ".delete" ).on( "click", function() {
      var listitem = $( this ).parent( "li.ui-li" );

      confirmAndDelete( listitem );
    });
  }


});


