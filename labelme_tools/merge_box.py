import argparse
import shutil
import errno
import time
import json
import glob
import os
import cv2
import base64


DEBUG = True

class MergeBox(object):

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


    def parse_file_list(self, input_dir, output_dir):
        """
        """

        label_file_list = glob.glob(os.path.join(input_dir, '*.txt'))

        for label_file in label_file_list:

            real_name = label_file.split('/')[-1].split('.')[0]

            image_file = os.path.join(input_dir, "{}.jpg".format(real_name))
            label_image_file = os.path.join(output_dir, "{}.jpg".format(real_name))
            print(image_file)
            if os.path.exists(image_file):
                self.draw_box(label_file, image_file, label_image_file)



    def draw_box(self, label_file, image_file, label_image_file):

        if not os.path.exists(label_file) or not os.path.exists(image_file):
            print('【警告】文件不存在  --------file:  {} '.format(label_file))
            #print(image_file)
            #print(json_file)
            return

        #########################
        #
        #########################
        with open(image_file, 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')



        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # print("++++++++++++++++++++")
        # print(len(lines))
        # print(lines)
        # print("++++++++++++++++++++")
        lines = self.do_merge_box(lines)

        #print("file: {}    word count: {} ".format(json_file, len(data['words_result'])))

        bg_image = cv2.imread(image_file)
        label_map = {"version": "4.0.0",
                     'flags': {},
                     "lineColor": [
                         0,
                         255,
                         0,
                         128
                     ],
                     "fillColor": [
                         255,
                         0,
                         0,
                         128
                     ],
                     'imagePath': image_file,
                     'imageData': image_base64,
                     'imageWidth': bg_image.shape[1],
                     'imageHeight': bg_image.shape[0]}

        for index, line in enumerate(lines):
            #print(line)
            if len(line) < 8:
                continue
            #
            # 117,7,230,7,230,46,117,46
            # print(item[1]['words'], item[1]['location'])
            points = line.split(',')
            left = int(points[0])
            width = int(points[2]) - int(points[0])
            top = int(points[1])
            height = int(points[7]) - int(points[1])

            #print(line, end='')

            colors = (0, 255, 0)
            cv2.rectangle(bg_image, (left, top), (left+width, top+height), colors, 1)



        cv2.imwrite(label_image_file, bg_image)
        print('【输出】生成合格后的图片{} .'.format(label_image_file))

    def box_to_line(self, box):
        return '{},{},{},{},{},{},{},{}'.format(
            box['left'],
            box['top'],
            box['right'],
            box['top'],
            box['right'],
            box['bottom'],
            box['left'],
            box['bottom'],)

    def delete_row_in_list(self, new_lines, line):

        for index, new_line in enumerate(new_lines):
            if line == new_line:
                print("find -------------------------- ", index)
                new_lines.remove(line)
                break



    def _do_merge_inline(self, new_lines):

        box_list = []
        box_map = {}
        new_lines.sort()
        # 生成合并的box 框
        for index, line in enumerate(new_lines):
            line = line.replace("\n", '')
            #print('index {}    [{}]'.format(index, line))
            points = line.split(',')
            if len(points) < 8:
                continue
            box = {
                'left': int(points[0]),
                'right': int(points[2]),

                'width': int(points[2]) - int(points[0]),
                'height': int(points[7]) - int(points[1]),

                'top': int(points[1]),
                'bottom': int(points[7])
            }
            box_list.append(box)
            box_map[self.box_to_line(box)] = False

        print("合并前Box 数量 : ", len(new_lines))
        print("合并前Box 数量 : ", len(box_list))
        # for line in new_lines:
        #     print(line)

        # 查找临近的box， 本次合并的box 数量
        total_count = 0

        new_box_lines = []
        for i in range(len(box_list)):
            if box_map[self.box_to_line(box_list[i])]:
                continue

            merge_flag = False

            for j in range(len(box_list)):
                if box_map[self.box_to_line(box_list[j])] or i == j:
                    continue
                if box_list[j]['width'] < 150 \
                        and box_list[i]['width'] < 150 \
                        and abs(box_list[j]['left'] - box_list[i]['right']) < 7 \
                        and abs(box_list[j]['top'] - box_list[i]['top']) < 8 \
                        and abs(box_list[j]['bottom'] - box_list[i]['bottom']) < 8:

                    # 添加新的box ， 删除两个旧的box

                    top = box_list[i]['top']
                    if box_list[j]['top'] < box_list[i]['top']:
                        top = box_list[j]['top']

                    bottom = box_list[i]['bottom']
                    if box_list[j]['bottom'] > box_list[i]['bottom']:
                        bottom = box_list[j]['bottom']


                    new_box = {
                        'left': box_list[i]['left'],
                        'right': box_list[j]['right'],

                        'width': box_list[j]['right'] - box_list[i]['left'],
                        'height': bottom - top,

                        'top': top,
                        'bottom': bottom
                    }

                    box_map[self.box_to_line(box_list[i])] = True
                    box_map[self.box_to_line(box_list[j])] = True
                    new_box_lines.append(self.box_to_line(new_box))
                    merge_flag = True

                    print('{} === {} '.format(self.box_to_line(box_list[i]), self.box_to_line(box_list[j])))
                    total_count += 1
            if not merge_flag:
                new_box_lines.append(self.box_to_line(box_list[i]))

        print("合并了 {}个 box".format(total_count))
        print("总共 {}个 box".format(len(new_box_lines)))
        return new_box_lines, total_count


    def do_merge_box(self, new_lines):

        new_lines, total_count = self._do_merge_inline(new_lines)
        new_lines, total_count = self._do_merge_inline(new_lines)
        new_lines, total_count = self._do_merge_inline(new_lines)

        return new_lines


    def main(self):
        time_start = time.time()
        # Argument parsing
        args = self.parse_arguments()
        if os.path.exists(args.output_dir):
            shutil.rmtree(args.output_dir)

        try:
            os.makedirs(args.output_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(args.input_dir):
            print("输入路径不能为空  input_dir[{}] ".format(args.input_dir))
            return
        self.parse_file_list(args.input_dir, args.output_dir)

        time_elapsed = time.time() - time_start
        print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))


if __name__ == "__main__":
    mergeBox = MergeBox()
    mergeBox.main()