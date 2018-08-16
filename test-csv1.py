#!/usr/bin/env python
#coding:utf-8
import jieba.analyse as analyse
from collections import Counter
import time
from os import path
import jieba
import importlib, sys
importlib.reload(sys)
import csv
import pandas as pd
from pandas import DataFrame

jieba.load_userdict("newdict.txt")
d = path.dirname(__file__)
filepath = r'C:\Users\Lenovo\zqrbtest\redup.csv'

def removdup():
    train = pd.read_csv(r'C:\Users\Lenovo\zqrbtest\data.csv')
    train = train['titlec']
    train = set(train)
    data = pd.DataFrame(list(train), columns=['titlec'])
    data.to_csv('redup.csv', index=False, encoding='utf_8_sig')
    
if __name__ == "__main__":
    def stopwordslist(filepath):
        stopwords = [line.strip()for line in open(filepath, 'r', encoding='utf-8').read().split('\n')]
        rs2 = []
        return stopwords
    def seg_sentence (sentence):
        sentence_seged = jieba.cut(sentence.strip())
        stopwords = stopwordslist('stop.txt')
        outstr = ''
        for word in sentence_seged:
            if word not in stopwords:
                if word != '\t':
                    outstr += word
                    outstr += " "
        return outstr
    inputs = open('redup.csv',  'r', encoding='utf-8')
    outputs = open('hel.csv', 'w', encoding='utf-8')
    for line in inputs:
        line_seg = seg_sentence(line)
        outputs.write(line_seg + '\n')
    outputs.close()
    inputs.close()


if __name__ == "__main__":
    aResult = removdup()
    csvfile = open('wordCount.csv', 'w', newline='', encoding='utf_8_sig')
    spamwriter = csv.writer(csvfile)
    word_list = []
    key_list = []
    for line in open('hel.csv', 'r', encoding='UTF-8'):
        item = line.strip('\n\r').split('\t')
        tags = jieba.analyse.extract_tags(item[0])
        for t in tags:
            word_list.append(t)

    word_dict = {}
    with open("result3.txt", 'w') as wf2:
        for item in word_list:
            if item not in word_dict:
                word_dict[item] = 1
            else:
                word_dict[item] += 1

        orderList = list(word_dict.values())
        orderList.sort(reverse=True)
        for i in range(len(orderList)):

            for key in word_dict:
                if word_dict[key] == orderList[i]:
                    wf2.write(key + ' ' + str(word_dict[key]) + '\n')
                    key_list.append(key)
                    word_dict[key] = 0

    for i in range(len(key_list)):
        spamwriter.writerow((key_list[i], orderList[i]))
    csvfile.close()
    
    rf_path = 'wordcount.csv'
    title = ['keyut', 'fre']

    r2g = pd.read_csv(rf_path, header=None)
    insertRow = pd.DataFrame([title])
    r2g = insertRow.append(r2g, ignore_index=True)
    df = r2g.to_csv('wordcount-1.csv', header=None, index=None, encoding='utf_8_sig')

    a = pd.read_csv('wordcount-1.csv')
    a.set_index('keyut')
    b = pd.read_csv('total.csv', encoding='utf_8_sig', engine='python')
    b.set_index('keyut')
    c = pd.merge(b, a, on='keyut', how='left')
    c.to_csv('collection.csv', encoding='utf_8_sig')
