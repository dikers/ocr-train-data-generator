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


python ../label_tools/generate_labelme_format.py \
--input_dir='../target/' \
--output_dir='../output/'