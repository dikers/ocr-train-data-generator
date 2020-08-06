import argparse
import shutil
import errno
import time
import json
import glob
import os
import cv2
import uuid

"""
将baidu ocr 格式转换成Textract 格式
"""

class OCRConver:
    def __init__(self):
        pass


    def parse_arguments(self):
        """
            Parse the command line arguments of the program.
        """

        parser = argparse.ArgumentParser(
            description="生成labelme 格式数据"
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



    def convert(self, file_name_source, file_name_dest, image_file):


        print(" file_name_source : ",  file_name_source)
        print(" file_name_dest : ",  file_name_dest)
        print(" image_file : ",  image_file)


        image = cv2.imread(image_file)
        size = image.shape
        width=size[1]
        height=size[0]
        print("width: {} height: {} ".format(width, height))

        result = {"DocumentMetadata": {"Pages": 1}, "JobStatus": "SUCCEEDED"}
        block_page = {"BlockType": "PAGE",
                      "Geometry": {"BoundingBox": {"Width": 1.0, "Height": 1.0, "Left": 0.0, "Top": 0.0},
                                   "Polygon": [{"X": 0.0, "Y": 0.0}, {"X": 1.0, "Y": 0.0}, {"X": 1.0, "Y": 1.0},
                                               {"X": 0.0, "Y": 1.0}]}, "Id": str(uuid.uuid4())}

        with open(file_name_source, 'r') as file:
            source = file.read()
        json_source = json.loads(source)
        words = json_source["words_result"]
        ids = []
        result["Blocks"] = [block_page]
        for word in words:
            block_word = {"BlockType": "WORD"}
            block_word["Confidence"] = word["probability"]["average"]
            block_word["Text"] = word["words"]
            source_location = word["location"]
            BoundingBox = {"Width": source_location["width"] / width, "Height": source_location["height"] / height,
                           "Left": source_location["left"] / width, "Top": source_location["top"] / height}
            Polygon_0 = {"X": source_location["left"] / width, "Y": source_location["top"] / height}
            Polygon_1 = {"X": (source_location["left"] + source_location["width"]) / width,
                         "Y": source_location["top"] / height}
            Polygon_2 = {"X": (source_location["left"] + source_location["width"]) / width,
                         "Y": (source_location["top"] + source_location["height"]) / height}
            Polygon_3 = {"X": source_location["left"] / width,
                         "Y": (source_location["top"] + source_location["height"]) / height}
            Polygon = [Polygon_0, Polygon_1, Polygon_2, Polygon_3]
            block_word["Geometry"] = {"BoundingBox": BoundingBox, "Polygon": Polygon}
            block_word_id = str(uuid.uuid4())
            block_word["Id"] = block_word_id
            block_word["Page"] = 1
            ids.append(block_word_id)
            result["Blocks"].append(block_word)

        block_page["Relationships"] = [{"Type": "CHILD", "Ids": ids}]
        block_page["Page"] = 1

        with open(file_name_dest, 'w', encoding='utf-8') as file:
            file.write(json.dumps(result))

    def main(self):
        time_start = time.time()
        # Argument parsing
        args = self.parse_arguments()
        if not os.path.exists(args.input_dir):
            print("输入路径不能为空  input_dir[{}] ".format(args.input_dir))
            return

        json_file_list = glob.glob(args.input_dir + '/*/data.json')


        for json_file in json_file_list:
            file_name_dest = os.path.join(args.input_dir, '_'.join(json_file.split('/')[-2].split('_')[:-2]) + '.json')
            image_file = os.path.join('/'.join(json_file.split('/')[:-1]), 'image.png')
            self.convert(json_file, file_name_dest, image_file)

        print(json_file_list)



        time_elapsed = time.time() - time_start
        print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

if __name__ == "__main__":

    convert = OCRConver()
    convert.main()
