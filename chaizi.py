from pypinyin import lazy_pinyin
import json
from datetime import datetime
import os
import textwrap

def todouble(s):
    """
    传入单汉字的全拼编码，反回其小鹤双拼编码，代码参考自：https://github.com/bcaso/pinyin_to_double_pinyin.git

    :param s: 全拼编码
    :return: 双拼编码

    """

    # 小鹤字典

    first = {'ch': 'i',
            'sh': 'u',
            'zh': 'v'}

    second = {
        'ua': 'x',
        'ei': 'w',
        'e': 'e',
        'ou': 'z',
        'iu': 'q',
        've': 't',
        'ue': 't',
        'u': 'u',
        'i': 'i',
        'o': 'o',
        'uo': 'o',
        'ie': 'p',
        'a': 'a',
        'ong': 's',
        'iong': 's',
        'ai': 'd',
        'ing': 'k',
        'uai': 'k',
        'ang': 'h',
        'uan': 'r',
        'an': 'j',
        'en': 'f',
        'ia': 'x',
        'iang': 'l',
        'uang': 'l',
        'eng': 'g',
        'in': 'b',
        'ao': 'c',
        'v': 'v',
        'ui': 'v',
        'un': 'y',
        'iao': 'n',
        'ian': 'm'
    }

    # 特殊，只有䪨母，且总长不过 3
    # 零声母，单双三䪨母
    special = {
        'a': 'aa',
        'ai': 'ai',
        'an': 'an',
        'ang': 'ah',
        'ao': 'ao',
        'e': 'ee',
        'ei': 'ei',
        'en': 'en',
        'er': 'er',
        'o': 'oo',
        'ou': 'ou'
    }

    new_s = ''
    # 特列情况: 无声母，a, an, ang
    if len(s) <= 3 and s[0] in ['a', 'e', 'o']:
        if s in special.keys():
            return special[s]
        else:
            print('未知情况1', s)

    # 一般: 声母 + 䪨母

    # 最长的情况：first+second，例如 chuang = ch + uang
    # 2 位声母 + 最多 4 位韵母
    if s[:2] in first.keys():
        new_s += first[s[:2]]
        # 最多 4 位䪨母
        if s[2:] in second.keys():
            new_s += second[s[2:]]
    # 较短的情况：second+second，例如 h uang, x iang
    # 1 位声母 + 最多 4 位䪨母
    else:
        new_s += s[0]  # 1 位声母
        # 最多 4 位䪨母
        if s[1:] in second.keys():
            new_s += second[s[1:]]
        else:
            new_s += s[1:]

    return new_s

def get_char_with_num_and_stroke():

    """
    获取汉字笔划数字典，代码参考自：https://github.com/taishan1994/stroke2vec.git
    """

    char_with_num_and_stroke = {}
    char_stroke_file_path = os.path.join(".", "data", "char_with_num_and_stroke.json")
    with open(char_stroke_file_path, 'r') as fp:
        char_with_num_and_stroke = json.loads(fp.read())
    return char_with_num_and_stroke

def get_stroke_num(s, char_with_num_and_stroke):
    """
    获取汉字笔划数，代码参考自：https://github.com/taishan1994/stroke2vec.git

    :param s: 汉字
    :return: 笔划数

    """

    return int(char_with_num_and_stroke[s.strip()]['num'])

def chai():
    """
    生成拆字字典，代码参考自：http://gerry.lamost.org/blog/?p=296003
    """
    
    chaizi_dict = os.path.join(".", "data", "chaizi-jt.txt")
    lines = open(chaizi_dict).readlines()   # 载入简体拆字字典
    yaml_path = os.path.join(".", "double_pinyin_flypy.chaizi.dict.yaml")
    dfile = open(yaml_path, 'w')     # 打开待写入字库文件

    # 字典头
    dfile.write(textwrap.dedent("""\
    name: double_pinyin_flypy.chaizi
    version: "%s"
    sort: by_weight
    use_preset_vocabulary: true
    ...
    """%(datetime.strftime(datetime.now(), "%Y-%m-%d"))))
    
    dfile.write("\n")

    # 获取汉字笔划数字典
    char_with_num_and_stroke = get_char_with_num_and_stroke()

    for line in lines:
        data = line.strip().split('\t')
        for i in range(1,len(data)):

            # 获取对应的拼音
            quanpins = lazy_pinyin(data[i].replace(" ",""))

            # 将拼音转化为双拼形式，使用小鹤双拼
            shuangpib = []
            for qp in quanpins:
                shuangpib.append(todouble(qp))

            ## 加入uu作为拆字字典开始
            py = "uu " + " ".join(shuangpib)

            ## 获取笔划数，若笔划数太少则删除
            stroke_num = 0
            try:
                stroke_num = get_stroke_num(data[0], char_with_num_and_stroke)
            except:
                stroke_num = 0

            # 生成rime词库要求格式，默认词频为1
            if py.replace(" ", "").isalpha() and stroke_num > 10:
                item = data[0].strip()+'\t'+py+'\t1\n'
                dfile.write(item)
            else:
                print(data[i])

    dfile.close()

def main():
    chai()


if __name__ == "__main__":
    main()