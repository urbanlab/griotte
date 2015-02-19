{
  "name": "speedy blink",
  "type": "block",
  "xml": "<block type=\"setinterval\" id=\"271\" inline=\"true\" x=\"156\" y=\"128\"><field name=\"handler\">handler</field><comment pinned=\"false\" h=\"149\" w=\"241\">Brancher une led sur l'entrée digital 3 de l'arduino </comment><value name=\"time\"><block type=\"math_number\" id=\"300\"><field name=\"NUM\">100</field></block></value><statement name=\"callback\"><block type=\"fwritedigital\" id=\"316\"><field name=\"valeur\">1</field><field name=\"pin\">3</field><next><block type=\"settimeout\" id=\"310\" inline=\"true\"><field name=\"handler\">handler</field><value name=\"time\"><block type=\"math_number\" id=\"311\"><field name=\"NUM\">50</field></block></value><statement name=\"callback\"><block type=\"fwritedigital\" id=\"317\"><field name=\"valeur\">0</field><field name=\"pin\">3</field></block></statement></block></next></block></statement></block>",
  "codejs": "var handler;\n\n\n// Brancher une led sur l'entrée digital 3 de l'arduino\nhandler = setInterval(function(){\n  fwriteDigital(3,1);handler = setTimeout(function(){\n    fwriteDigital(3,0);},50);\n}\n,100);\n",
  "codepy": ""
}