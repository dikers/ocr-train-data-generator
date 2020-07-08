import os
import argparse
import sys


class ConvertEncoding(object):
    def __init__(self):
        args = self.parse_arguments()
        self.input_dir = args.input_dir

    def parse_arguments(self):
        """
            Parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            description="把JSON文件从UTF-8转化为GBK"
        )
        parser.add_argument(
            "-i",
            "--input_dir",
            type=str,
            nargs="?",
            help="输入文件路径",
            required=True
        )
        return parser.parse_args()

    def __doConvert(self, file):
        src_file = os.path.join(self.input_dir, file)
        file_data = ""
        with open(src_file, 'r', encoding='utf-8') as f:
            for line in f:
                file_data += line
        with open(src_file, 'w', encoding='gbk') as f:
            f.write(file_data)

    def convert(self):
        dir = self.input_dir
        dir_list = os.listdir(dir)
        for cur_file in dir_list:
            if cur_file.endswith("json"):
                self.__doConvert(cur_file)


if __name__ == "__main__":
    if sys.platform == "win32":
        convert = ConvertEncoding()
        convert.convert()
    else:
        print("非windows环境，无需转化")
