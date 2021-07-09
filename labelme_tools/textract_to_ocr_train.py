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
        
        parser.add_argument(
            "-f",
            "--fixed_height",
            type=int,
            nargs="?",
            help="输出图片的固定高度",
            default=48
        )
        
        parser.add_argument(
            "-c",
            "--confidence_threshold",
            type=float,
            nargs="?",
            help="输出图片的固定高度",
            default=0.98
        )

        return parser.parse_args()


    def parse_file_list(self, input_dir, output_dir):
        """
        """

        #print(" input dir: {} ".format(input_dir))
        dirs = os.listdir(input_dir)
        types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(os.path.join(input_dir, files)))

        files_grabbed.sort()
        total_correct_lines = ''
        total_wrong_lines = ''
        for index, file in enumerate(files_grabbed):
            json_file = os.path.join(input_dir, file.split('/')[-1].split('.')[0] + '.json')
            
            if os.path.exists(json_file):
                correct_lines, wrong_lines = self.create_label(json_file, file, output_dir)
                total_correct_lines += correct_lines
                total_wrong_lines += wrong_lines
            else:
                print("  {} 不存在 ".format(json_file))

        correct_gt_labels_file = os.path.join(self.output_dir_correct, 'label.txt')
        wrong_gt_labels_file = os.path.join(self.output_dir_wrong, 'label.txt')
        with open(correct_gt_labels_file, "w") as f:
            f.write(total_correct_lines)
            print('【输出】生成 lambelme 格式文件  输出路径{}, 文件个数 {} , 识别正确文件大小 {}.'.format(correct_gt_labels_file, 
                                                                                len(files_grabbed), len(total_correct_lines)))

        with open(wrong_gt_labels_file, "w") as f:
            f.write(total_wrong_lines)
            print('【输出】生成 lambelme 格式文件  输出路径{}, 文件个数 {} , 识别错误文件大小 {}.'.format(wrong_gt_labels_file, 
                                                                                len(files_grabbed), len(total_wrong_lines)))
    
            

    def create_label(self, json_file, image_file, output_dir):

    #         print("----------      {}     ".format(json_file))
        if not os.path.exists(json_file) or not os.path.exists(image_file):
            print('【警告】文件不存在  --------file:  {} '.format(json_file))
            #print(image_file)
            #print(json_file)
            return

        with open(json_file, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

        bg_image = cv2.imread(image_file)


        image_height = bg_image.shape[0]
        image_width = bg_image.shape[1]
        print('{}  width={} height={}'.format(image_file, image_width, image_height))

        
        
        wrong_lines = ''
        correct_lines = ''

        for index, item in enumerate(json_data['Blocks']):
            if item['BlockType'] != "WORD" :
                continue

            points = item['Geometry']['Polygon'] 
            #print(points)
            left = int(points[0]['X'] * image_width)

            if int(points[1]['X'] * image_width ) < left:
                left = int(points[1]['X'] * image_width)

            top = int(points[0]['Y'] * image_height)

            if int(points[1]['Y'] * image_height) < top:
                size = bg_image.shape
                top = int(points[1]['Y'] * image_height) 


            width = int(abs(points[1]['X']  - points[0]['X']) * image_width)
            height = int(abs(points[3]['Y']  - points[0]['Y']) * image_height)
            text = item['Text'].lstrip().rstrip()




            c_img = bg_image[int(top): int(top + height), int(left): int(left + width)]
            sub_image_name = 'image/' + image_file.split('/')[-1].replace('.', '_')+'_'+str(index).zfill(5)+".jpg"

            if c_img.shape[0] < 10 or c_img.shape[1] < 10:
                continue

            scale = self.fixed_height / height
            new_w, new_h = int(width * scale), self.fixed_height
            resize_img = cv2.resize(c_img, (new_w, new_h))
            print("top={} left={} width={} height={}  confidence={} text:[{}]  file: {} ".format(top, left, new_w, new_h, item['Confidence'], text, sub_image_name))

            
            if item['Confidence']< self.confidence_threshold :
                cv2.imwrite(os.path.join(self.output_dir_wrong,  sub_image_name), resize_img)
                line = "{}\t{}\t{}\n".format(sub_image_name, text, item['Confidence'])
                wrong_lines += line
                
            else:
                cv2.imwrite(os.path.join(self.output_dir_correct,  sub_image_name), resize_img)
                line = "{}\t{}\n".format(sub_image_name, text)
                correct_lines += line

        return correct_lines, wrong_lines


    def main(self):
        time_start = time.time()
        # Argument parsing
        args = self.parse_arguments()
        if os.path.exists(args.output_dir):
            shutil.rmtree(args.output_dir)

        try:
            
            self.output_dir = args.output_dir
            self.output_dir_correct = os.path.join(args.output_dir,"correct") 
            self.output_dir_wrong   = os.path.join(args.output_dir,"wrong") 
            os.makedirs(os.path.join(self.output_dir_correct,"image"))
            os.makedirs(os.path.join(self.output_dir_wrong,"image"))
            
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if not os.path.exists(args.input_dir):
            print("输入路径不能为空  input_dir[{}] ".format(args.input_dir))
            return
    
        self.fixed_height            = args.fixed_height
        self.confidence_threshold    = args.confidence_threshold
        print("fixed_height:[{}]   confidence_threshold:[{}]".format(self.fixed_height, self.confidence_threshold))
        
        self.parse_file_list(args.input_dir, args.output_dir)

        time_elapsed = time.time() - time_start
        print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))


if __name__ == "__main__":
    generateLabelmeFormat = GenerateLabelmeFormat()
    generateLabelmeFormat.main()