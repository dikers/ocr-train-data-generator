echo $#  '生成ocr训练数据'
if [ $# -ne 1 ]
then
    echo "Usage: $0  包含图片的文件夹 "
    exit
fi


export PYTHONPATH=../



python ../label_tools/ocr.py \
--input_dir=$1 \
--output_dir='../target/' \
--app_id='' \
--api_key='' \
--secret_key=''


python ../labelme_tools/labelme_to_ocr_train.py \
--input_dir='../target/' \
--output_dir='../output/'


#python ../label_tools/convert_encoding.py --input_dir='../output/'

python ../labelme_tools/convert_to_textract.py \
--input_dir='../target/'