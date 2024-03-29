# ocr-train-data-generator
ocr 模型训练数据生成工具


### 调用第三方自动生成训练样本


[百度OCR api 接口](https://ai.baidu.com/ai-doc/OCR/)


申请 开发ID 和Key
```python
from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '你的 App ID'
API_KEY = '你的 Api Key'
SECRET_KEY = '你的 Secret Key'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
```



### 修改 label_tools/run.sh

注意代码执行路径在 ./label_tools 下面

```shell script

cd  label_tools
sh ./run.sh '需要识别的图片文件夹路径'

```




### 生成数据示例样本
`./output/`  输出的图片和json格式数据， 供labelme 使用

```
test001.jpg
test001.json
test002.jpg
test002.json
```

用labelme 工具 打开 `../output/` 文件夹

[Labelme 数据标注工具](https://github.com/wkentaro/labelme)


### Textract 格式数据生成训练数据


```
cd label_tools
sh textract.sh
```

textract.sh 会运行下面的程序， 修改相关参数
```
# input_dir   图片和识别后的json 文件 保存路径， 在一个文件夹下， json 是textract 格式
# output_dir   输出文件路径
# -c  置信度阈值 confidence_threshold = 0.98
# -f  输出图片的固定高度  fixed_height = 48

python ../labelme_tools/textract_to_ocr_train.py \
--input_dir='../../ocr_data/001/image' \
--output_dir='../../ocr_data/001/output/' \
-f=48 \
-c=0.99
```


