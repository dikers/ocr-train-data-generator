import os
import argparse
import sys
import glob


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

    def _do_convert(self, json_file, encoding):
        print(json_file)
        file_data = ""
        with open(json_file, 'r', encoding='utf-8') as f:
            for line in f:
                file_data += line
        with open(json_file, 'w', encoding=encoding) as f:
            f.write(file_data)

    def convert(self):
        if self.encoding == "utf-8":
            print("输出格式为utf-8，不需要转化")
        elif self.encoding == 'gbk':
            json_list = glob.glob(os.path.join(self.input_dir, '*.json'))
            for json_file in json_list:
                self._do_convert(json_file, 'gbk')
            print("{}个文件已转化为{} ".format(len(json_list), self.encoding))
        else:
            print("不能识别的编码格式 [{}]".format(self.encoding))

if __name__ == "__main__":
    convert = ConvertEncoding()
    convert.convert()
