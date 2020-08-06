
import random
import time
random.seed(time.time())


def create_zero(count):
    char_list = '0Oo***.\、.----。、~!O@0o/L#$%0/LOg/Lo^./L**&00.00*()0。g/L、、--/L---+|/0Oo[]#%$￥0~-/L--！/L@#oo*~~~￥0O%&*OO。[]0Oog/L'
    lines = ''
    for i in range(count):
        # print("{}   random {}".format(i, random.randint(3, 10)))
        line_length = random.randint(3, 10)
        line = ''
        for j in range(line_length):
            start = random.randint(0, len(char_list) -2)
            line += char_list[start: start+2]
        #print(line)
        lines += (line +'\n')
    return lines


def create_char(count):


    start_char = '#%!~*-^*/+#%*、，。.*.。*'
    char_list = 'ABCDEFGHIJKLMNOPQRSTUVWXYZA'
    lines = ''
    for i in range(count):
        line_length = random.randint(3, 8)
        line = start_char[random.randint(0, len(start_char)-1)]
        for j in range(line_length):
            line += char_list[random.randint(0, len(char_list)-1)]
        #print(line)
        lines += (line +'\n')

    return lines

def create_method_1(count):

    char_split = ['--', '~', '--', '%', '/L', 'g/L', 'mg/L', 'L/L', '^', '=>', '<=', '*', '、', '。']
    lines = ''
    for i in range(count):
        a = random.randint(10, 100000) / 1000
        b = random.randint(10, 100000) / 1000
        lines += "{}{}{}\n".format(a, char_split[random.randint(0, len(char_split)-1)], b)

    return lines

def create_number_1(count):
    char_list = '.。,壹贰叁肆伍陆柒捌玖拾佰仟.。,一二三四五六七八九十元百千万亿.。/,1234567890.。,、**%~##'

    lines = ''
    for i in range(count):
        line_length = random.randint(3, 8)
        line = ''
        for j in range(line_length):
            line += char_list[random.randint(0, len(char_list)-1)]
        #print(line)
        lines += (line +'\n')

    return lines

def create_number_2(count):
    char_list = '+-*/%￥￥￥$$$***... 。。。、、、~~~***--%%%***、~~=@#'
    lines = ''
    for i in range(count):
        line = '{}{}{}'.format(random.randint(0,100000)/1000.0,
                               char_list[random.randint(0, len(char_list)-1)],
                               random.randint(0,100000)/1000.0)
        lines += (line +'\n')

    return lines


if __name__ == "__main__":

    labels_file = '../output/spec_chars_02.txt'

    total_lines = ''
    #total_lines += create_number_2(200)
    total_lines += create_zero(3000)
    #total_lines += create_char(200)
    total_lines += create_method_1(2000)
    # print(total_lines)

    lines = total_lines.split('\n')

    print("length : {} ".format(len(lines)))

    line_list = []
    for line in lines:

        if len(line) < 1:
            continue
        line_list.append(line)


    line_list = list(set(line_list))

    random.shuffle(line_list)
    lines = '\n'.join(line_list)
    #print(lines)


    with open(labels_file, "w") as f:
        f.write(lines)
        print('【输出】生成文件  输出路径{}, 对象个数 {}.'.format(labels_file, len(line_list)))



