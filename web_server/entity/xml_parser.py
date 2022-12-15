from datetime import timedelta


def convert_string_to_timedelta(date_time_as_string: str) -> timedelta:
    """
    Converts a date time string into a timedelta, ignores the date part of the
    string
    :param date_time_as_string: time as string as in 20221207 12:21:37.881
    :return: a timedelta for time part of the string, 12:21:37.881
    """
    time = date_time_as_string.split(" ")[1]
    hh_mm_ss = time.split(".")[0].split(":")
    ms = time.split(".")[1]

    return timedelta(
        hours=int(hh_mm_ss[0]),
        minutes=int(hh_mm_ss[1]),
        seconds=int(hh_mm_ss[2]),
        milliseconds=int(ms)
    )


class XMLParser:
    def __init__(self, object_from_xml):
        """
        Parser for Robot XML object
        :param object_from_xml: Python object from a Robot XML file
        """
        self.obj = object_from_xml
        self.vtt_entry = f'<count>\n<start-time> --> <end-time>\n<keyword>\n\n'

    def get_video_url(self,test_name):
        for test in self.obj.robot.suite.suite.suite.test:
            if test['name'] == test_name:
                return test.doc.cdata.split("[")[1].split("|")[0]
        return None

    def get_test_names(self):
        """
        :return: a list of the names of the test cases
        """
        return [test["name"] for test in self.obj.robot.suite.suite.suite.test]

    def generate_vtt(self, test_name):
        """
        Generates the VTT entries for a test case
        :param test_name: the test case name
        :return: a list of VTT entries
        """
        vtt_list = ['WEBVTT\n\n\n']
        elapse_time = timedelta()

        for test in self.obj.robot.suite.suite.suite.test:
            if test['name'] == test_name:
                for kw in test.kw:
                    if kw["name"] != "Run Keywords":
                        entry, elapse_time = self.make_a_vtt_entry(elapse_time, kw, len(vtt_list))
                        vtt_list.append(entry)
                    else:
                        for kw1 in kw.kw:
                            entry, elapse_time = self.make_a_vtt_entry(elapse_time, kw1, len(vtt_list))
                            vtt_list.append(entry)
        return vtt_list

    def make_a_vtt_entry(self, elapse_time, keyword, count):
        entry = self.vtt_entry
        entry = entry.replace('<count>', f'{count - 1}')

        ms = int(elapse_time.microseconds / 1000)
        h_mm_ss = str(elapse_time).split(".")[0]
        entry = entry.replace('<start-time>', f'0{h_mm_ss}.{ms:03d}')

        start = convert_string_to_timedelta(keyword.status["starttime"])
        end = convert_string_to_timedelta(keyword.status["endtime"])
        elapse_time += end - start
        ms = int(elapse_time.microseconds / 1000)
        h_mm_ss = str(elapse_time).split(".")[0]
        entry = entry.replace('<end-time>', f'0{h_mm_ss}.{ms:03d}')

        keyword_name = keyword["name"]
        if keyword["name"] in ["Run Setup Keyword", "Run Cleanup Keyword"]:
            keyword_name = f'{keyword["name"]}  {keyword.arguments.children[0].cdata}'
            if keyword.arguments.children[0].cdata == 'sleep':
                keyword_name = f'{keyword["name"]} {keyword.arguments.children[0].cdata} ' \
                               f'{keyword.arguments.children[1].cdata}s'

        entry = entry.replace('<keyword>', keyword_name)
        return entry, elapse_time
