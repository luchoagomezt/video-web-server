from urllib3.exceptions import NewConnectionError

from web_server.entity.xml_parser import XMLParser
import untangle
import requests


class VTTVideo:
    def __init__(self):
        self.parser = None
        self.test_case_name = ""
        self.test_case_names = []
        self.vtt_list = []
        self.video_url = ""

    def set_parser(self, file_name):
        self.parser = XMLParser(untangle.parse(file_name))
        self.test_case_names = self.parser.get_test_names()

    def set_test_case_name(self, test_case_name):
        self.test_case_name = test_case_name

    def get_test_name(self):
        return self.test_case_name

    def get_test_names(self):
        return self.test_case_names

    def generate_vtt_list(self):
        if self.parser is not None and self.test_case_name != "":
            self.vtt_list = self.parser.generate_vtt(self.test_case_name)

    def get_vtt_list(self):
        return self.vtt_list

    def set_video_url(self):
        if self.parser is not None and self.test_case_name != "":
            self.video_url = self.parser.get_video_url(self.test_case_name)

    def save_video_to_file(self, video_file_name):
        status = 500

        if self.video_url != "":
            try:
                response = requests.get(self.video_url)
            except Exception:
                return status

            with open(video_file_name, 'wb') as fp:
                for chunk in response.iter_content(chunk_size=128):
                    fp.write(chunk)

            return response.status_code

        return status

    def save_vtt_list_to_file(self, vtt_file_name):
        with open(vtt_file_name, 'w') as fp:
            for entry in self.vtt_list:
                fp.write(entry)
            fp.close()
