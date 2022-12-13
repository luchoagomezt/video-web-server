from web_server.entity.xml_parser import XMLParser
import untangle
import os


def test_generate_vtt():
    config_directory = os.path.dirname(os.path.realpath(__file__))
    xml_file = os.path.join(os.path.dirname(config_directory), "unit/original.xml")

    robot_xml_object = untangle.parse(xml_file)
    xml_parser = XMLParser(robot_xml_object)
    vtt = xml_parser.generate_vtt("MEDQA 339 Add a professional")

    assert len(vtt) == 21
    assert "0" in vtt[1]
    assert "00:00:00.000 --> 00:00:09.004" in vtt[1]
    assert "Login as Super Administrator" in vtt[1]
    assert "19" in vtt[20]
    assert "00:00:58.533 --> 00:01:02.657" in vtt[20]
    assert "Cleanup" in vtt[20]