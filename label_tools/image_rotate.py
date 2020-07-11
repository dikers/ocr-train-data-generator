from PIL import Image
import piexif
import argparse
import os
import glob
import shutil
"""
旋转图片
left:  头部向左
right: 头部向右
180:   头部向下
normal:  正常
"""

class ImageRotate(object):
    def __init__(self):
        args = self.parse_arguments()
        self.input_dir = args.input_dir
        self.output_dir = args.output_dir
        self.unknown_dir = os.path.join(args.input_dir, 'unknown')

    def parse_arguments(self):
        """
            Parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            description="旋转图片"
        )
        parser.add_argument(
            "-i",
            "--input_dir",
            type=str,
            nargs="?",
            help="输入文件路径 包含子文件夹 'left', 'right', '180', 'normal'  ",
            default='./input'
        )
        parser.add_argument(
            "-o",
            "--output_dir",
            type=str,
            nargs="?",
            help="输出文件路径",
            default='./datasets'
        )

        return parser.parse_args()

    def rotate_image(self, image_file, output_dir,  rotate_type):
        if rotate_type not in ('left', 'right', '180', 'normal'):
            print("旋转类型不正确 文件夹路径不正确  {} ".format(rotate_type))
            return

        target_file = os.path.join(output_dir, rotate_type + "_"+image_file.split('/')[-1])
        if 'normal' == rotate_type:
            shutil.copy(image_file, target_file)
            return


        im = Image.open(image_file)

        if "exif" in im.info:

            # shutil.copy(image_file, os.path.join(self.unknown_dir, rotate_type + "_"+image_file.split('/')[-1] ))
            exif_dict = piexif.load(im.info["exif"])
        else:
            exif_dict = {}
            exif_dict["0th"] = {}


        # print(type(exif_dict), exif_dict)

        # for ifd in ("0th", "Exif", "GPS", "1st"):
        # for ifd in ("0th", "Exif"):
        #     for tag in exif_dict[ifd]:
        #         print(piexif.TAGS[ifd][tag], exif_dict[ifd][tag])

        exif_dict["0th"][piexif.ImageIFD.Orientation] = 1


        if rotate_type == "right":
            im = im.transpose(Image.ROTATE_90)
        elif rotate_type == "left":
            im = im.transpose(Image.ROTATE_270)
        elif rotate_type == "180":
            im = im.transpose(Image.ROTATE_180)
        else:
            print("【Error】 file {}  type {} ".format(image_file ,rotate_type))


        exif_bytes = piexif.dump(exif_dict)
        #print("File {}  原始方向 {} ".format(image_file, rotate_type))

        im.save(target_file, exif=exif_bytes)

    def rotate_dir(self, rotate_type):
        base_dir =os.path.join(self.input_dir, rotate_type)
        #print(base_dir)
        if not os.path.exists(base_dir):
            return
        types = ('*.JPG', '*.PNG', '*.JPEG', '*.jpg', '*.png', '*.jpeg')
        files_grabbed = []
        for files in types:
            files_grabbed.extend(glob.glob(os.path.join(base_dir, files)))

        for index, file in enumerate(files_grabbed):
            self.rotate_image(file, self.output_dir, rotate_type)

        print("Rotate type [{}], 共有文件数量: {} ".format(rotate_type , len(files_grabbed)))

    def main(self):

        print("output_dir  {} ".format(self.output_dir))
        if not os.path.exists(self.output_dir):
            print("-------------")
            os.mkdir(self.output_dir)

        if not os.path.exists(self.unknown_dir):
            os.mkdir(self.unknown_dir)

        self.rotate_dir('left')
        self.rotate_dir('right')
        self.rotate_dir('180')
        self.rotate_dir('normal')




if __name__ == "__main__":
    imageRotate = ImageRotate()
    imageRotate.main()


