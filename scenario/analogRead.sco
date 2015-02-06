{
  "name": "analog read",
  "type": "block",
  "xml": "<block type=\"readanalog\" id=\"9\" x=\"169\" y=\"27\"><field name=\"VAR\">valeur</field><field name=\"channel\">1</field><statement name=\"callback\"><block type=\"text_print\" id=\"10\" inline=\"false\"><value name=\"TEXT\"><block type=\"variables_get\" id=\"11\"><field name=\"VAR\">valeur</field></block></value></block></statement></block>",
  "codejs": "var valeur;\n\n\nreadAnalog(1,function(valeur){\n  print(valeur);\n});\n",
  "codepy": ""
}