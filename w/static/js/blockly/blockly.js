/**
 * Create a namespace for the application.
 */
var Code = {};

/**
 * List of tab names.
 * @private
 */
Code.TABS_ = ['javascript', 'xml'];

Code.selected = 'javascript';

/**
 * Switch the visible pane when a tab is clicked.
 * @param {string} clickedName Name of tab clicked.
 */
Code.tabClick = function(clickedName) {
  // If the XML tab was open, save and render the content.
  if (document.getElementById('tab_xml').className == 'tabon') {
    //var xmlTextarea = document.getElementById('content_xml');
    //var xmlText = xmlTextarea.value;
    var xmlText = Code.xmleditor.getValue()
    var xmlDom = null;
    try {
      xmlDom = Blockly.Xml.textToDom(xmlText);
    } catch (e) {
      var q =
          //window.confirm(MSG['badXml'].replace('%1', e));
          window.confirm('bad xml');
      if (!q) {
        // Leave the user on the XML tab.
        return;
      }
    }
    if (xmlDom) {
      Blockly.mainWorkspace.clear();
      Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
    }
  }

  // Deselect all tabs and hide all panes.
  for (var i = 0; i < Code.TABS_.length; i++) {
    var name = Code.TABS_[i];
    document.getElementById('tab_' + name).className = 'taboff';
    document.getElementById('content_' + name).style.visibility = 'hidden';
  }

  // Select the active tab.
  Code.selected = clickedName;
  document.getElementById('tab_' + clickedName).className = 'tabon';
  // Show the selected pane.
  document.getElementById('content_' + clickedName).style.visibility =
      'visible';
  Code.renderContent();
  Blockly.fireUiEvent(window, 'resize');
};

/**
 * Populate the currently selected pane with content generated from the blocks.
 */
Code.renderContent = function() {
  var content = document.getElementById('content_' + Code.selected);
  // Initialize the pane.
  if (content.id == 'content_xml') {
    //var xmlTextarea = document.getElementById('content_xml');
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);
    //xmlTextarea.value = xmlText;
    //xmlTextarea.focus();
    Code.xmleditor.setValue(xmlText,-1);
    //Code.xmleditor.setValue("<hello></hello>",-1);
  } else if (content.id == 'content_javascript') {
    var code = Blockly.JavaScript.workspaceToCode();
    //content.textContent = code;
    Code.jseditor.setValue(code,-1);
    /*if (typeof prettyPrintOne == 'function') {
      code = content.innerHTML;
      code = prettyPrintOne(code, 'js');
      content.innerHTML = code;
    }*/
  }
};

/**
 * Bind a function to a button's click event.
 * On touch enabled browsers, ontouchend is treated as equivalent to onclick.
 * @param {!Element|string} el Button element or ID thereof.
 * @param {!Function} func Event handler to bind.
 */
Code.bindClick = function(el, func) {
  if (typeof el == 'string') {
    el = document.getElementById(el);
  }
  el.addEventListener('click', func, true);
  el.addEventListener('touchend', func, true);
};



/**
 * Initialize Blockly.  Called on page load.
 */
Code.init = function() {

  Code.tabClick(Code.selected);
  Blockly.fireUiEvent(window, 'resize');

  for (var i = 0; i < Code.TABS_.length; i++) {
    var name = Code.TABS_[i];
    Code.bindClick('tab_' + name,
        function(name_) {return function() {Code.tabClick(name_);};}(name));
  }

};
