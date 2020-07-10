import os
import argparse
import sys


class ConvertEncoding(object):
    def __init__(self):
        args = self.parse_arguments()
        self.input_dir = args.input_dir
        self.encoding = args.encoding
        if self.encoding is None:
            self.encoding = "utf-8"

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
        parser.add_argument(
            "-e",
            "--encoding",
            type=str,
            nargs="?",
            help="输出文件编码格式",
            required=False
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
        if self.encoding == "utf-8":
            print("输出格式为utf-8，不需要转化")
        else:
            dir = self.input_dir
            dir_list = os.listdir(dir)
            for cur_file in dir_list:
                if cur_file.endswith("json"):
                    self.__doConvert(cur_file)
            print("已转化为"+self.encoding)


if __name__ == "__main__":
    convert = ConvertEncoding()
    convert.convert()
