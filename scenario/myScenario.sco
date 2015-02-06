{
  "name": "my scenario",
  "type": "block",
  "xml": "<block type=\"controls_if\" id=\"1\" inline=\"false\" x=\"178\" y=\"132\"><value name=\"IF0\"><block type=\"logic_boolean\" id=\"2\"><field name=\"BOOL\">TRUE</field></block></value><statement name=\"DO0\"><block type=\"text_print\" id=\"3\" inline=\"false\"><value name=\"TEXT\"><block type=\"text\" id=\"4\"><field name=\"TEXT\">okido</field></block></value></block></statement></block>",
  "codejs": "if (true) {\n  window.alert('okido');\n}\n",
  "codepy": "def run():\n  if True:\n    print('okido')\n  \n\n\nif __name__ == \"__main__\":\n  from griotte.config import Config\n  Config(\"DEFAULT\")\n  run()"
}