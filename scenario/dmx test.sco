{
  "name": "dmx test",
  "type": "block",
  "xml": "<block type=\"dmx_send_channels\" id=\"1\" inline=\"false\" x=\"407\" y=\"101\"><value name=\"VALUES\"><block type=\"lists_create_with\" id=\"2\" inline=\"false\"><mutation items=\"2\"></mutation><value name=\"ADD0\"><block type=\"math_number\" id=\"3\"><field name=\"NUM\">255</field></block></value><value name=\"ADD1\"><block type=\"math_number\" id=\"4\"><field name=\"NUM\">255</field></block></value></block></value><value name=\"CHANNELS\"><block type=\"lists_create_with\" id=\"6\" inline=\"false\"><mutation items=\"3\"></mutation><value name=\"ADD0\"><block type=\"math_number\" id=\"7\"><field name=\"NUM\">2</field></block></value><value name=\"ADD1\"><block type=\"math_number\" id=\"8\"><field name=\"NUM\">4</field></block></value><value name=\"ADD2\"><block type=\"math_number\" id=\"9\"><field name=\"NUM\">6</field></block></value></block></value></block>",
  "codejs": "sendDmxM({\"2\":\"255\",\"4\":\"255\",\"6\":0})\n",
  "codepy": ""
}