{
  "name": "tempo",
  "type": "block",
  "xml": "<block type=\"setinterval\" id=\"32\" inline=\"true\" x=\"383\" y=\"41\"><field name=\"handler\">handler</field><value name=\"time\"><block type=\"math_number\" id=\"33\"><field name=\"NUM\">1000</field></block></value><statement name=\"callback\"><block type=\"text_print\" id=\"34\" inline=\"false\"><value name=\"TEXT\"><block type=\"text\" id=\"35\"><field name=\"TEXT\">It's about time !!</field></block></value></block></statement></block><block type=\"ondigitalchange\" id=\"36\" x=\"848\" y=\"41\"><field name=\"channel\">DIP0</field><field name=\"VAR\">v</field><statement name=\"callback\"><block type=\"text_print\" id=\"37\" inline=\"false\"><value name=\"TEXT\"><block type=\"text\" id=\"38\"><field name=\"TEXT\">STOOOOOOP !</field></block></value><next><block type=\"clearinterval\" id=\"39\"><field name=\"handler\">handler</field></block></next></block></statement></block>",
  "codejs": "var handler;\nvar v;\n\n\nhandler = setInterval(function(){\n  print('It\\'s about time !!');\n},1000);\n\nonDigitalChange(\"DIP0\",function(v){\n  print('STOOOOOOP !');\n  clearInterval(handler);\n});\n",
  "codepy": ""
}