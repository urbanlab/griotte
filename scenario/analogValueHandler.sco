{
  "name": "analog handler",
  "type": "block",
  "xml": "<block type=\"onanalog\" id=\"4\" x=\"209\" y=\"49\"><field name=\"VAR\">v</field><field name=\"channel\">0</field><statement name=\"callback\"><block type=\"text_print\" id=\"5\" inline=\"false\"><value name=\"TEXT\"><block type=\"text_join\" id=\"6\" inline=\"false\"><mutation items=\"2\"></mutation><value name=\"ADD0\"><block type=\"text\" id=\"7\"><field name=\"TEXT\">sur le an 0 :</field></block></value><value name=\"ADD1\"><block type=\"variables_get\" id=\"8\"><field name=\"VAR\">v</field></block></value></block></value></block></statement></block>",
  "codejs": "var v;\n\n\nonAnalog(0,function(v){\n  print(String('sur le an 0 :') + String(v));\n});\n",
  "codepy": ""
}