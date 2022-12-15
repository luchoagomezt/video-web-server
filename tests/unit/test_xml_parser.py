from _pytest.python_api import raises

from web_server.entity.xml_parser import XMLParser
import untangle
import os

xml_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                        "unit/original_one_suite.xml")
robot_xml_object = untangle.parse(xml_file)

def test_empty_object():
    with raises(AssertionError):
        XMLParser(None)


def test_generate_vtt():
    xml_parser = XMLParser(robot_xml_object)
    vtt = xml_parser.generate_vtt("MEDQA 339 Add a professional")

    test_names = xml_parser.get_test_names()
    assert len(test_names) == 8
    assert len(vtt) == 21
    assert "0" in vtt[1]
    assert "00:00:00.000 --> 00:00:09.004" in vtt[1]
    assert "Login as Super Administrator" in vtt[1]
    assert "19" in vtt[20]
    assert "00:00:58.533 --> 00:01:02.657" in vtt[20]
    assert "Cleanup" in vtt[20]


def test_multiple_suites_generate_vtt():
    xml_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                            "unit/original_multiple_suites.xml")
    robot_xml_object = untangle.parse(xml_file)
    xml_parser = XMLParser(robot_xml_object)

    test_names = xml_parser.get_test_names()
    assert len(test_names) == 490

    test1 = "MEDQA 205 Add an appointment from the patient file using green plus"
    vtt_205 = xml_parser.generate_vtt(test1)
    assert len(vtt_205) == 13
    assert "00:00:00.000 --> 00:00:10.455" in vtt_205[1]
    assert "7" in vtt_205[8]
    assert "Verify Appointment Data Form Open" in vtt_205[8]

    test2 = "MEDQA 33 Modify an appointment from the Agenda"
    vtt_33 = xml_parser.generate_vtt(test2)
    assert len(vtt_33) == 12
    assert "1" in vtt_33[2]

    test3 = "MEDQA 2764 Add active medication manually from note summary widget without prescription"
    vtt_2764 = xml_parser.generate_vtt(test3)
    assert len(vtt_2764) == 1

    test4 = "MEDQA 821 Set up a professional to work with all patients from the patient portal"
    vtt_821 = xml_parser.generate_vtt(test4)
    assert len(vtt_821) == 21
    assert "10" in vtt_821[11]
    assert "00:00:11.763 --> 00:00:15.111" in vtt_821[8]

    test5 = "MEDQA 820 Set up an office to work with patient portal"
    vtt_820 = xml_parser.generate_vtt(test5)
    assert len(vtt_820) == 18
    assert "0" in vtt_820[1]


def test_get_test_names():
    xml_parser = XMLParser(robot_xml_object)
    names = xml_parser.get_test_names()

    assert len(names) == 8
    assert "MEDQA 339 Add a professional" in names


def test_get_video_url():
    xml_parser = XMLParser(robot_xml_object)
    url= xml_parser.get_video_url("MEDQA 339 Add a professional")
    assert url == "http://10.63.0.248/videos/MEDQA_339_Add_a_professional_20221207172400.mp4"


def test_get_video_url_multiple_suites():
    xml_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                            "unit/original_multiple_suites.xml")
    robot_xml_object = untangle.parse(xml_file)
    xml_parser = XMLParser(robot_xml_object)
    url = xml_parser.get_video_url("MEDQA 821 Set up a professional to work with all patients from the patient portal")
    assert url == "http://10.63.0.246/videos/MEDQA_821_Set_up_a_professional_to_work_with_all_patients_from_the_patient_portal_20221214080614.webm"
