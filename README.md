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