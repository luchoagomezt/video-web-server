from web_server.entity.xml_parser import XMLParser
import untangle
import os

xml_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                        "unit/original.xml")
robot_xml_object = untangle.parse(xml_file)


def test_generate_vtt():
    xml_parser = XMLParser(robot_xml_object)
    vtt = xml_parser.generate_vtt("MEDQA 339 Add a professional")

    assert len(vtt) == 21
    assert "0" in vtt[1]
    assert "00:00:00.000 --> 00:00:09.004" in vtt[1]
    assert "Login as Super Administrator" in vtt[1]
    assert "19" in vtt[20]
    assert "00:00:58.533 --> 00:01:02.657" in vtt[20]
    assert "Cleanup" in vtt[20]


def test_get_test_names():
    xml_parser = XMLParser(robot_xml_object)
    names = xml_parser.get_test_names()

    assert len(names) == 8
    assert "MEDQA 339 Add a professional" in names


def test_get_video_url():
    xml_parser = XMLParser(robot_xml_object)
    url= xml_parser.get_video_url("MEDQA 339 Add a professional")
    assert url == "http://10.63.0.248/videos/MEDQA_339_Add_a_professional_20221207172400.mp4"
