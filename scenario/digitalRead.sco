{
  "name": "digital read",
  "type": "block",
  "xml": "<block type=\"readdigital\" id=\"11\" x=\"185\" y=\"88\"><field name=\"VAR\">v</field><field name=\"channel\">DIP0</field><statement name=\"callback\"><block type=\"text_print\" id=\"12\" inline=\"false\"><value name=\"TEXT\"><block type=\"variables_get\" id=\"13\"><field name=\"VAR\">v</field></block></value></block></statement></block>",
  "codejs": "var v;\n\n\nreadDigital(\"DIP0\",function(v){\n  print(v);\n});\n",
  "codepy": ""
}