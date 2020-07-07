export PYTHONPATH=../

python ../label_tools/ocr.py \
--input_dir='../dataset/' \
--output_dir='../target/' \
--app_id='' \
--api_key='' \
--secret_key=''


python ../label_tools/generate_labelme_format.py \
--input_dir='../target/' \
--output_dir='../output/'