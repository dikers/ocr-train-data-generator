import json
import uuid
import cv2

"""
将baidu ocr 格式转换成Textract 格式
"""

class OCRConver:
    def __init__(self, file_name_source, file_name_dest, image_file):
        self.file_source = file_name_source
        self.file_dest = file_name_dest

        image = cv2.imread(image_file)
        size = image.shape
        self.width=size[1]
        self.height=size[0]
        print("width: {} height: {} ".format(self.width, self.height))

    def __loadSource(self):
        with open(self.file_source, 'r') as file:
            source = file.read()
        return source


    def __write_result(self,result):
        with open(self.file_dest, 'w', encoding='utf-8') as file:
            file.write(json.dumps(result))


    def convert(self):
        width=self.width
        height=self.height
        result = {"DocumentMetadata": {"Pages": 1}, "JobStatus": "SUCCEEDED"}
        block_page = {"BlockType": "PAGE",
                      "Geometry": {"BoundingBox": {"Width": 1.0, "Height": 1.0, "Left": 0.0, "Top": 0.0},
                                   "Polygon": [{"X": 0.0, "Y": 0.0}, {"X": 1.0, "Y": 0.0}, {"X": 1.0, "Y": 1.0},
                                               {"X": 0.0, "Y": 1.0}]}, "Id": str(uuid.uuid4())}

        source = self.__loadSource()
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
        self.__write_result(result)


if __name__ == "__main__":
    image_file = '../dataset/07_26/test002.jpg'
    data_file = '../dataset/07_26/data.json'
    output_file = '../dataset/07_26/textract.json'
    convert=OCRConver(data_file,output_file, image_file )
    convert.convert()
