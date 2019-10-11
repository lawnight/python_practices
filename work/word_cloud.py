# 生成词云
import json
import unicodedata
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from fnmatch import fnmatch
import os
from collections import defaultdict
from keras.preprocessing.text import Tokenizer

textFile = 'work/report.txt' 

def cut_words(text,add_words=[]):
    for word in add_words:
        jieba.add_word(word)
    seg_list = jieba.cut(text, cut_all=False)
    return seg_list

def getWordCloud(talk):
     return WordCloud(font_path=r'D:\code\simfang.ttf').generate(talk)


with open(textFile,encoding='utf8') as f:
    text = f.read()
    seg = cut_words(text)

    topic = ' '.join(seg)
    
    samples = [topic]
    tokenizer = Tokenizer(num_words=1000)
    tokenizer.fit_on_texts(samples)
    sequences = tokenizer.texts_to_sequences(samples)
    one_hot_results = tokenizer.texts_to_matrix(samples,mode='binary')

    print(one_hot_results)


    # img = getWordCloud(''.join(seg))
    # plt.imshow(img)
    # plt.show()
