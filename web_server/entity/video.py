import untangle

from datetime import timedelta
import os.path
import filecmp


def convert_to_time(time_as_string: str) -> timedelta:
    time = time_as_string.split(" ")[1]
    ms = time.split(".")[1]
    total = time.split(".")[0].split(":")

    # create timedelta
    td = timedelta(
        seconds=int(total[2]),
        milliseconds=int(ms),
        minutes=int(total[1]),
        hours=int(total[0]),
    )
    return td


class Video:
    def __init__(self, test_name):
        self.test_name = test_name
        self.CONFIG_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
        self.xmlFile = os.path.join(os.path.dirname(self.CONFIG_DIRECTORY), "model/original.xml")
        self.obj = untangle.parse(self.xmlFile)


    def get_video_file_name(self):
        return "videos/" + self.test_name + '.webm'

    def get_track_file_name(self):
        return "videos/" + self.test_name + '.vtt'

    def get_test_names(self):
        tests = [test["name"] for test in self.obj.robot.suite.suite.suite.test]
        print(tests)
        return tests

        # tests = [test["name"] for test in obj.robot.suite.suite.suite.test]
        # save_path = '../static/videos'
        # complete_name = os.path.join(save_path, "test_name.txt")
        # f = open(complete_name, "w")
        # for test in obj.robot.suite.suite.suite.test:
        #     f.write(test["name"])
        #     f.write("\n")
        #
        # f.close()

    def generate_vtt_file(self):

        complete_name = os.path.join(os.path.dirname(self.CONFIG_DIRECTORY), "static/videos/" + self.test_name + ".vtt")

        f = open(complete_name, "w")
        f.write('WEBVTT\n\n\n')
        count = 0
        current = timedelta()

        for test in self.obj.robot.suite.suite.suite.test:
            if test['name'] == self.test_name:
                for kw in test.kw:
                    if kw["name"] != "Run Keywords":
                        f.write(f'{count}\n')
                        ms = int(current.microseconds / 1000)

                        f.write(f'0{str(current).split(".")[0]}.{ms:03d}')
                        f.write(' --> ')
                        count += 1
                        start = convert_to_time(kw.status["starttime"])
                        end = convert_to_time(kw.status["endtime"])
                        current += end - start

                        ms = int(current.microseconds / 1000)

                        f.write(f'0{str(current).split(".")[0]}.{ms:03d}\n')
                        f.write(f'{kw["name"]}\n\n')
                    else:
                        for kw1 in kw.kw:
                            f.write(f'{count}\n')
                            ms = int(current.microseconds / 1000)

                            f.write(f'0{str(current).split(".")[0]}.{ms:03d}')
                            f.write(' --> ')
                            count += 1

                            start = convert_to_time(kw1.status["starttime"])
                            end = convert_to_time(kw1.status["endtime"])
                            current += end - start

                            ms = int(current.microseconds / 1000)

                            f.write(f'0{str(current).split(".")[0]}.{ms:03d}\n')

                            if kw1.arguments.children[0].cdata == 'sleep':
                                f.write(f'{kw1.arguments.children[0].cdata} for {kw1.arguments.children[1].cdata}s\n\n')
                            else:
                                f.write(f'{kw1.arguments.children[0].cdata}\n\n')
        f.close()



if __name__ == '__main__':
    video = Video('MEDQA 339 Add a professional')
    video.generate_vtt_file('../model/original.xml')
    video.generate_test_name_file()
    #video.get_test_names("../static/videos/test_name.txt")
    #video.get_test_names("../view/test_name.txt")
    assert (filecmp.cmp("../static/videos/MEDQA 339 Add a professional(1).vtt",
                        "../static/videos/MEDQA 339 Add a professional.vtt"))
