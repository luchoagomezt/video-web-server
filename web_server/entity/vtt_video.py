from web_server.entity.xml_parser import XMLParser
import untangle


class VTTVideo:
    def __init__(self):
        self.parser = None
        self.test_case_name = ""
        self.test_case_names = []
        self.vtt_list = []

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

    def save_vtt_list_to_file(self, vtt_file_name):
        with open(vtt_file_name, 'w') as fp:
            for entry in self.vtt_list:
                fp.write(entry)
            fp.close()
