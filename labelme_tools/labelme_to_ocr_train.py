import argparse
import shutil
import errno
import time
import json
import glob
import os
import cv2
import math


DEBUG = True

class GenerateLabelmeFormat(object):

    def __init__(self):
        args = self.parse_arguments()
        self.output_dir = args.output_dir
        self.input_dir = args.input_dir

    def parse_arguments(self):
        """
            Parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            description="生成labelme 格式数据"
        )
        parser.add_argument(
            "-o",
            "--output_dir",
            type=str,
            nargs="?",
            help="输出文件的本地路径",
            required=True
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


    def parse_file_list(self, input_dir):
        """
        """

        #print(" input dir: {} ".format(input_dir))
        dirs = os.listdir(input_dir)
        types = ('*.pdf', '*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(os.path.join(input_dir, files)))

        total_lines = ''
        for index, file in enumerate(files_grabbed):
            json_file = os.path.join(input_dir, file.split('/')[-1].split('.')[0] + '.json')
            print(json_file)
            if os.path.exists(json_file):
                new_lines = self.create_label(json_file, file, )
                total_lines += new_lines

        gt_labels_file = os.path.join(self.output_dir, 'label.txt')
        with open(gt_labels_file, "w") as f:
            f.write(total_lines)
            print('【输出】生成 lambelme 格式文件  输出路径{}, 对象个数 {}.'.format(gt_labels_file, len(files_grabbed)))

    def create_label(self, json_file, image_file):

        print("----------      {}     ".format(json_file))
        if not os.path.exists(json_file) or not os.path.exists(image_file):
            print('【警告】文件不存在  --------file:  {} '.format(json_file))
            #print(image_file)
            #print(json_file)
            return

        with open(json_file, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

        bg_image = cv2.imread(image_file)

        new_lines = ''
        for index, item in enumerate(json_data['shapes']):
            #print(item['points'], item['label'])
            left = int(item['points'][0][0])

            if int(item['points'][1][0]) < left:
                print("error top ")
                left = item['points'][1][0]

            top = int(item['points'][0][1])

            if int(item['points'][1][1]) < top:
                size = bg_image.shape

                w = size[1] #宽度

                h = size[0] #高度

                print(size)
                print(w)
                print(h)
                print("error top   w {} h {} ".format(w, h))
                print(" top: {}   left: {}   width: {}  height:  {}".format(top, left, width, height))
                top = item['points'][1][1]


            width = abs(int(item['points'][1][0]) - int(item['points'][0][0]))
            height = abs(int(item['points'][1][1]) - int(item['points'][0][1]))

            if left < 0 or height < 10 or width < 10:
                print(" top: {}   left: {}   width: {}  height:  {}".format(top, left, width, height))
                continue


            text = item['label'].lstrip().rstrip()
            c_img = bg_image[int(top): int(top + height), int(left): int(left + width)]
            sub_image_name = image_file.split('/')[-1].replace('.', '_')+'_'+str(index).zfill(5)+".jpg"

            if c_img.shape[0] < 10 or c_img.shape[1] < 10:
                continue

            cv2.imwrite(os.path.join(self.output_dir,  sub_image_name), c_img)

            line = "{} {}\n".format(sub_image_name, text)
            new_lines += line


        return new_lines


    def main(self):
        time_start = time.time()
        # Argument parsing
        args = self.parse_arguments()
        if os.path.exists(args.output_dir):
            shutil.rmtree(args.output_dir)

        try:
            os.makedirs(args.output_dir)
            self.output_dir = args.output_dir
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(args.input_dir):
            print("输入路径不能为空  input_dir[{}] ".format(args.input_dir))
            return
        self.parse_file_list(args.input_dir)

        time_elapsed = time.time() - time_start
        print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))


if __name__ == "__main__":
    generateLabelmeFormat = GenerateLabelmeFormat()
    generateLabelmeFormat.main()