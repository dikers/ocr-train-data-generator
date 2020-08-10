import argparse
import shutil
import errno
import time
import glob
import os
import cv2
import numpy as np

from merge_tools import do_merge_box


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
            return

        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        lines = do_merge_box(lines)

        bg_image = cv2.imread(image_file)
        raw_image = cv2.imread(image_file)


        for index, line in enumerate(lines):
            if len(line) < 8:
                continue

            points = line.split(',')
            left = int(points[0]) if int(points[6]) > int(points[0]) else int(points[6])
            right = int(points[2]) if int(points[4]) < int(points[2]) else int(points[4])
            top = int(points[1]) if int(points[3]) > int(points[1]) else int(points[3])
            bottom = int(points[5]) if int(points[7]) < int(points[5]) else int(points[7])
            height = bottom - top
            width = right - left

            colors = (0, 0, 255)
            if index == 189:
                print(line)
                print("left={}  right={}  top={} bottom={}".format(left, right, top, bottom))




            # cv2.fillPoly(bg_image, [pts], (255, 255, 255))
            roi_corners=np.array([[(int(points[0]), int(points[1])),
                                   (int(points[2]), int(points[3])),
                                   (int(points[4]), int(points[5])),
                                   (int(points[6]), int(points[7]))]], dtype=np.int32)
            mask = np.ones(bg_image.shape, dtype=np.uint8)
            channels=bg_image.shape[2]
            #输入点的坐标
            channel_count=channels
            ignore_mask_color = (255,)*channel_count
            #创建mask层
            cv2.fillPoly(mask, roi_corners, ignore_mask_color)
            #为每个像素进行与操作，除mask区域外，全为0
            masked_image = cv2.bitwise_and(bg_image, mask)
            c_img = masked_image[top: int(top + height), left: int(left + width)]
            cv2.imwrite(os.path.join(self.output_dir, '{}.jpg'.format(index)), c_img)

            # 画矩形框
            pts = np.array([[int(points[0]), int(points[1])],
                            [int(points[2]), int(points[3])],
                            [int(points[4]), int(points[5])],
                            [int(points[6]), int(points[7])]], np.int32)  # 每个点都是(x, y)
            pts = roi_corners.reshape((-1, 1, 2))
            cv2.polylines(bg_image, [pts], True, (0, 0, 255))
            # cv2.rectangle(bg_image, (left, top), (left+width, top+height), colors, 1)


        cv2.imwrite(label_image_file, bg_image)
        print('【输出】生成合格后的图片{} .'.format(label_image_file))



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