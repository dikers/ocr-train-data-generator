import json
import cv2
import argparse
import shutil
import os
import time
import errno
import glob




class DataClean(object):

    def __init__(self):
        args = self.parse_arguments()
        self.output_dir = args.output_dir
        self.input_dir = args.input_dir
        self.mask_keys = args.mask_keys.split(',')
        self.box_distance = args.box_distance
        print("mask keys  : ", self.mask_keys)

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
        parser.add_argument(
            "-k",
            "--mask_keys",
            type=str,
            nargs="?",
            help="被屏蔽的关键字列表",
            default='姓名,住院'
        )
        parser.add_argument(
            "-d",
            "--box_distance",
            type=float,
            help="屏蔽字段的百分比距离",
            default=0.15
        )

        return parser.parse_args()

    def create_single_box(self, block, image_width, image_height):
        points = block['Geometry']['Polygon'];
        x0 = points[0]['X']
        y0 = points[0]['Y']

        x1 = points[1]['X']
        y1 = points[1]['Y']

        x2 = points[2]['X']
        y2 = points[2]['Y']

        x3 = points[3]['X']
        y3 = points[3]['Y']

        # print("a大于b") if a>b else ( print("a小于b") if a<b else print("a等于b") )
        top = y0
        if y1 < y0:
            top = y1

        left = x0
        if x3 < x0:
            left = x3

        right = x1
        if x2 > x1:
            right = x2

        bottom = y2
        if y3 > y2:
            bottom = y3

        box = {
            'left': int(image_width * left),
            'top': int(image_height * top),
            'right': int(image_width * right),
            'bottom': int(image_height * bottom),
            'text': block['Text'],
            'width': int(image_width * block['Geometry']['BoundingBox']['Width']),
            'height': int(image_height * block['Geometry']['BoundingBox']['Height']),
            'bounding_box': block['Geometry']['BoundingBox']
        }
        #print(box)

        return box


    def get_image_size(self, image_file):
        bg_image = cv2.imread(image_file)
        size = bg_image.shape
        width = size[1] #宽度
        height = size[0] #高度
        return bg_image, width, height

    def find_mask_box(self, all_box):
        mask_box = []
        for box in all_box:
            for label in self.mask_keys:
                if label in box['text']:
                    mask_box.append(box)
                    break
        return mask_box



    def find_next_mask_box(self, all_box_list, mask_box_list):

        next_box_list = []
        for box in mask_box_list:
            for _box in all_box_list:
                if box['left'] == _box['left']:
                    continue

                if _box['bounding_box']['Left'] - box['bounding_box']['Left'] < self.box_distance \
                        and _box['left'] > box['right'] \
                        and abs(_box['top'] - box['top']) < box['height'] \
                        and abs(_box['bottom'] - box['bottom']) < box['height']:
                    print('前一个box [{}]   后一个box [{}] '.format(box['text'], _box['text']))
                    next_box_list.append(_box)
                    continue
        return next_box_list



    def clean_mask_box(self, image_file, mask_box, label_image_file):

        bg_image = cv2.imread(image_file)
        for box in mask_box:
            print(box)
            colors = (255, 255, 255)
            cv2.rectangle(bg_image, (box['left'], box['top']),
                          (box['right'], box['bottom']), colors, -1)

        cv2.imwrite(label_image_file, bg_image)
        print('【输出】脱敏后的图片  {} .'.format(label_image_file))


    def create_box(self, json_file, width, height):
        with open(json_file, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

        blocks = json_data['Blocks']

        all_box = []
        for block in blocks:
            if not block['BlockType'] == 'WORD':
                continue

            all_box.append(self.create_single_box(block, width, height))

        return all_box

    def parse_file_list(self):

        types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(os.path.join(self.input_dir, files)))

        image_map_list = []
        for index, file in enumerate(files_grabbed):
            temp_name = file.split('/')[-1].split('.')[0]
            print()
            image_file = file

            json_file = os.path.join(self.input_dir, temp_name+'.json')
            print(json_file)
            if os.path.exists(json_file):
                image_map_list.append((image_file, json_file))

        return image_map_list

    def generate_clean_image(self, image_map_list):

        print('-' * 50)
        print('| generate_clean_image', ' ' * (50-len('generate_clean_image') -4) +'|')
        print('-' * 50)
        for index, item in enumerate(image_map_list):
            image_file, json_file = item[0], item[1]
            clean_image_file = os.path.join(self.output_dir, image_file.split("/")[-1])
            print('处理第{}张图片   {} '.format(index+1, image_file))
            bg_image, image_width, image_height = self.get_image_size(image_file)
            all_box_list = self.create_box(json_file, image_width, image_height)
            mask_box_list = self.find_mask_box(all_box_list)

            next_box_list = self.find_next_mask_box(all_box_list, mask_box_list)
            mask_box_list.extend(next_box_list)
            self.clean_mask_box(image_file, mask_box_list, clean_image_file)


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
        image_map_list = self.parse_file_list()

        self.generate_clean_image(image_map_list)

        time_elapsed = time.time() - time_start
        print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))



if __name__ == "__main__":
    dataClean = DataClean()
    dataClean.main()









# all_box = create_box(json_file, image_width, image_height)
# #print(all_box)
# mask_box = find_mask_box(all_box)
#
# next_boxs = find_next_mask_box(all_box, mask_box)
# mask_box.extend(next_boxs)
# clean_mask_box(image_file, mask_box, label_image_file)
