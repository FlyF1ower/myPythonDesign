#!/usr/bin/env python
# -*- coding: utf-8  -*-
# 逐行读取文件数据进行jieba分词
import json

import jieba
import jieba.analyse
import codecs, sys, string, re


# 文本分词
def prepareData(sourceFile: str, targetFile: str):
    f = codecs.open(sourceFile, 'r', encoding='utf-8')
    target = codecs.open(targetFile, 'w', encoding='utf-8')
    print('open source file: ' + sourceFile)
    print('open target file: ' + targetFile)

    lineNum = 1
    line = f.readline()  # line这边可以优化写法
    while line:
        print('---processing ', lineNum, ' article---')
        line = clearTxt(line)
        seg_line = sent2word(line)
        target.writelines(seg_line + '\n')
        lineNum = lineNum + 1
        line = f.readline()
    print('well done.')
    f.close()
    target.close()


# 清洗文本
def clearTxt(line):
    if line != '':
        line = line.strip()
        intab = ""
        outtab = ""
        # trantab: dict = str.maketrans(intab, outtab)  # maketrans用于映射，两个字符串等长，对应位置映射
        bytes_trantab = bytes.maketrans(str.encode(intab), str.encode(outtab))
        pun_num: str = string.punctuation + string.digits  # punctuation是所有标点符号
        pun_num_bin = str.encode(pun_num)
        line = line.encode('utf-8')
        line = line.translate(bytes_trantab, pun_num_bin)
        line = line.decode("utf8")
        # 去除文本中的英文和数字
        line = re.sub("[a-zA-Z0-9]", "", line)
        # 去除文本中的中文符号和英文符号
        # line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+".decode("utf8"), "", line)
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line)
    return line


# 文本切割
def sent2word(line):
    segList = jieba.cut(line, cut_all=False)
    segSentence = ''
    for word in segList:
        if word != '\t':
            segSentence += word + " "
    return segSentence.strip()


if __name__ == '__main__':
    sourceFile = '2000_neg.txt'
    targetFile = '2000_neg_cut.txt'
    prepareData(sourceFile, targetFile)

    sourceFile = '2000_pos.txt'
    targetFile = '2000_pos_cut.txt'
    prepareData(sourceFile, targetFile)
