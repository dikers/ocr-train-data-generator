import os
import glob
import shutil


label_file = '/Users/dikers/work/datasets/medical/label.txt'
image_dir = '/Users/dikers/work/datasets/medical/medical_sub'


split_count = 1000
output_dir = '/Users/dikers/work/datasets/medical/split/'


if os.path.exists(output_dir):
    shutil.rmtree(output_dir)

os.makedirs(output_dir)


with open(label_file, 'r', encoding='utf8')as fp:
    lines = fp.readlines()



print(len(lines))


lines = list(set(lines))

new_lines = ''
for index, line in enumerate(lines):
    #print(line)


    new_lines += line
    if (index+1) % split_count == 0:
        sub_dir = os.path.join(output_dir, 'sub_{}'.format(index+1))
        os.mkdir(sub_dir)
        new_label_file = os.path.join( sub_dir, 'label.txt')
       # print('new_label_file', new_label_file)


        line_list = new_lines.split('\n')
        line_list.sort()

        new_lines = ''
        for new_line in line_list:

            image_file = new_line.split(' ')[0]
            if len(image_file) < 5:
                continue
            new_lines += (new_line+'\n')

            if os.path.exists(os.path.join(image_dir, image_file)):
                #print(os.path.join(image_dir, image_file), os.path.join(sub_dir, image_file) )
                shutil.copy(os.path.join(image_dir, image_file), os.path.join(sub_dir, image_file))

        with open(new_label_file , "w") as f:
            f.write(new_lines)

        new_lines = ''




