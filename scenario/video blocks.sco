{
  "name": "video blocks",
  "type": "block",
  "xml": "<block type=\"ondigitalchange\" id=\"3\" x=\"163\" y=\"56\"><field name=\"channel\">DIP0</field><field name=\"VAR\">v</field><statement name=\"callback\"><block type=\"controls_if\" id=\"4\" inline=\"false\"><mutation else=\"1\"></mutation><value name=\"IF0\"><block type=\"logic_compare\" id=\"5\" inline=\"true\"><field name=\"OP\">EQ</field><value name=\"A\"><block type=\"variables_get\" id=\"6\"><field name=\"VAR\">v</field></block></value><value name=\"B\"><block type=\"math_number\" id=\"7\"><field name=\"NUM\">1</field></block></value></block></value><statement name=\"DO0\"><block type=\"video_pause\" id=\"8\"></block></statement><statement name=\"ELSE\"><block type=\"video_resume\" id=\"9\"></block></statement></block></statement></block><block type=\"ondigitalchange\" id=\"10\" x=\"406\" y=\"225\"><field name=\"channel\">DIP1</field><field name=\"VAR\">v</field><statement name=\"callback\"><block type=\"controls_if\" id=\"11\" inline=\"false\"><mutation else=\"1\"></mutation><value name=\"IF0\"><block type=\"logic_compare\" id=\"12\" inline=\"true\"><field name=\"OP\">EQ</field><value name=\"A\"><block type=\"variables_get\" id=\"13\"><field name=\"VAR\">v</field></block></value><value name=\"B\"><block type=\"math_number\" id=\"14\"><field name=\"NUM\">1</field></block></value></block></value><statement name=\"DO0\"><block type=\"video_play\" id=\"15\"><field name=\"VIDEO\">/home/pi/media/sintel_trailer-720p.mp4</field><field name=\"loop_cb\">TRUE</field></block></statement><statement name=\"ELSE\"><block type=\"video_stop\" id=\"16\"></block></statement></block></statement></block>",
  "codejs": "var v;\n\n\nonDigitalChange(\"DIP0\",function(v){\n  if (v == 1) {\n    pauseMedia();\n  } else {\n    resumeMedia();\n  }\n});\n\nonDigitalChange(\"DIP1\",function(v){\n  if (v == 1) {\n    playMediaLoop('/home/pi/media/sintel_trailer-720p.mp4');\n  } else {\n    stopMedia();\n  }\n});\n",
  "codepy": ""
}