{
  "name": "relais clignotte",
  "type": "block",
  "xml": "<block type=\"variables_set\" id=\"119\" inline=\"true\" x=\"466\" y=\"141\"><field name=\"VAR\">RelayState</field><value name=\"VALUE\"><block type=\"math_number\" id=\"187\"><field name=\"NUM\">0</field></block></value><next><block type=\"writedigital\" id=\"102\"><field name=\"valeur\">0</field><field name=\"channel\">IO3</field><next><block type=\"setinterval\" id=\"100\" inline=\"true\"><field name=\"handler\">RelayState</field><comment pinned=\"false\" h=\"80\" w=\"160\">comment</comment><value name=\"time\"><block type=\"math_number\" id=\"101\"><field name=\"NUM\">500</field></block></value><statement name=\"callback\"><block type=\"controls_if\" id=\"128\" inline=\"false\"><mutation else=\"1\"></mutation><value name=\"IF0\"><block type=\"logic_compare\" id=\"140\" inline=\"true\"><field name=\"OP\">EQ</field><value name=\"A\"><block type=\"variables_get\" id=\"145\"><field name=\"VAR\">RelayState</field></block></value><value name=\"B\"><block type=\"math_number\" id=\"146\"><field name=\"NUM\">0</field></block></value></block></value><statement name=\"DO0\"><block type=\"variables_set\" id=\"148\" inline=\"true\"><field name=\"VAR\">RelayState</field><value name=\"VALUE\"><block type=\"math_number\" id=\"149\"><field name=\"NUM\">1</field></block></value><next><block type=\"writedigital\" id=\"147\"><field name=\"valeur\">1</field><field name=\"channel\">IO3</field></block></next></block></statement><statement name=\"ELSE\"><block type=\"variables_set\" id=\"154\" inline=\"true\"><field name=\"VAR\">RelayState</field><value name=\"VALUE\"><block type=\"math_number\" id=\"155\"><field name=\"NUM\">0</field></block></value><next><block type=\"writedigital\" id=\"156\"><field name=\"valeur\">0</field><field name=\"channel\">IO3</field></block></next></block></statement></block></statement></block></next></block></next></block>",
  "codejs": "var RelayState;\n\n\nRelayState = 0;\nwriteDigital(\"IO3\",0);// comment\nRelayState = setInterval(function(){\n  if (RelayState == 0) {\n    RelayState = 1;\n    writeDigital(\"IO3\",1);} else {\n    RelayState = 0;\n    writeDigital(\"IO3\",0);}\n}\n,500);\n",
  "codepy": ""
}