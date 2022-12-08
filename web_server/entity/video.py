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
        self.xmlFile = 'model/original.xml'

    def get_video_file_name(self):
        return "videos/" + self.test_name + '.webm'

    def get_track_file_name(self):
        return "videos/" + self.test_name + '.vtt'

    def generate_vtt_file(self, xml):
        obj = untangle.parse(xml)
        save_path = '../static/videos'
        complete_name = os.path.join(save_path, self.test_name + ".vtt")

        f = open(complete_name, "w")
        f.write('WEBVTT\n\n\n')
        count = 0
        current = timedelta()
        first = True

        for test in obj.robot.suite.suite.suite.test:
            if test['name'] == self.test_name:
                for kw in test.kw:
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

if __name__ == '__main__':
    video = Video('MEDQA 339 Add a professional')
    video.generate_vtt_file('../model/original.xml')
    assert (filecmp.cmp("../static/videos/MEDQA 339 Add a professional(1).vtt",
                        "../static/videos/MEDQA 339 Add a professional.vtt"))
