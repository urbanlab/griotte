{
  "name": "images",
  "type": "block",
  "xml": "<block type=\"setinterval\" id=\"19\" inline=\"true\" x=\"303\" y=\"58\"><field name=\"handler\">handler</field><value name=\"time\"><block type=\"math_number\" id=\"45\"><field name=\"NUM\">1000</field></block></value><statement name=\"callback\"><block type=\"image_play\" id=\"14\"><field name=\"IMAGE\">/home/pi/media/croco.jpg</field><next><block type=\"settimeout\" id=\"24\" inline=\"true\"><field name=\"handler\">handler</field><value name=\"time\"><block type=\"math_number\" id=\"74\"><field name=\"NUM\">500</field></block></value><statement name=\"callback\"><block type=\"image_play\" id=\"26\"><field name=\"IMAGE\">/home/pi/media/tumblr_mmabytqarU1ra4livo1_500.jpg</field></block></statement></block></next></block></statement></block>",
  "codejs": "var handler;\n\n\nhandler = setInterval(function(){\n  playMedia('/home/pi/media/croco.jpg');\n  handler = setTimeout(function(){\n    playMedia('/home/pi/media/tumblr_mmabytqarU1ra4livo1_500.jpg');\n  },500);\n}\n,1000);\n",
  "codepy": ""
}