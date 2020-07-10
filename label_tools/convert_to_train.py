#! /usr/bin/env python3
# coding=utf-8
import os
import argparse
import json
from shutil import copyfile
import sys


class ConvertLabelmeToTrain(object):
    def __init__(self):
        args = self.parse_arguments()
        self.input_dir = args.input_dir
        self.output_dir = args.output_dir
        self.encoding = args.encoding
        if self.encoding is None:
            self.encoding = "utf-8"

    def parse_arguments(self):
        """
            Parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            description="把Labelme格式文件转化为训练数据"
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
            "-o",
            "--output_dir",
            type=str,
            nargs="?",
            help="输出文件路径",
            required=True
        )
        parser.add_argument(
            "-e",
            "--encoding",
            type=str,
            nargs="?",
            help="输入文件编码格式",
            required=False
        )
        return parser.parse_args()

    def __loadSource(self,input_file):
        with open(input_file, 'r',encoding=self.encoding) as file:
            source = file.read()
        return source

    def __doImage(self,file):
        input_file = os.path.join(self.input_dir, file)
        output_file = os.path.join(self.output_image, file)
        copyfile(input_file,output_file)

    def __doConvert(self, file):
        input_file = os.path.join(self.input_dir, file)
        output_file = os.path.join(self.output_txt, file[:-4]+"txt") # 更改后缀
        source = self.__loadSource(input_file)
        json_source = json.loads(source)
        with open(output_file, 'w', encoding='utf-8') as f:
            for shape in json_source["shapes"]:
                point1=shape["points"][0]
                x1,y1=point1[0],point1[1]
                point2=shape["points"][1]
                x2,y2=point2[0],point2[1]
                point={"x1":x1,"y1":y1,"x2":x2,"y2":y2,"name":shape["label"]}
                f.writelines("{x1},{y1},{x2},{y1},{x2},{y2},{x1},{y2},{name}\n".format(**point))

    def __init_folder(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        output_image = os.path.join(self.output_dir, "ch4_training_images")
        self.output_image = output_image
        if not os.path.exists(output_image):
            os.mkdir(output_image)
        output_txt = os.path.join(self.output_dir,"ch4_training_localization_transcription_gt")
        self.output_txt = output_txt
        if not os.path.exists(output_txt):
            os.mkdir(output_txt)

    def convert(self):
        self.__init_folder()
        dir = self.input_dir
        dir_list = os.listdir(dir)
        for cur_file in dir_list:
            if cur_file.endswith("json"):
                self.__doConvert(cur_file)
            elif cur_file.endswith("jpg"):
                self.__doImage(cur_file)


if __name__ == "__main__":
    convert = ConvertLabelmeToTrain()
    convert.convert()

