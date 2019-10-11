#解析剧本，用jieba分词，并且画出词语
#%%
import xxtea
import pandas as pd
import json
import unicodedata
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from fnmatch import fnmatch
import os
from collections import defaultdict


userdict_list = ['信长','信长大人','家康大人']
stopwords_path='work\stop'

def jieba_processing_txt(text,add_words = []):

    for word in add_words:
        jieba.add_word(word)
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    
    # 停用词
    # with open(stopwords_path, encoding='utf-8') as f_stop:
    #     f_stop_text = f_stop.read()
    #     f_stop_seg_list = f_stop_text.splitlines()

    # for myword in liststr.split('/'):
    #     if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
    #         mywordlist.append(myword)
    return ' '.join(seg_list)

# 读取剧本
key = 'jgbw2eu3fhk4sb5g'

fpath = r'D:\code\war_mix_server\client\Documents\reading_story'


man_talk = defaultdict(list)

def parse_file(story_path):
    file = os.path.join(fpath,story_path)
    with open(file,'rb') as f:
        text = f.read()
        original = xxtea.decrypt(text,key,False)
        
        original = original.decode('utf8')
        lines = original.splitlines()
        #去掉末尾的脏字符
        lines[-1] = '}' 

        x= ''.join(lines)
        table = json.loads(x)
        
        df = pd.DataFrame(table)
        df = df.T             
        df.to_csv(os.path.join(fpath,story_path+'.csv'))
        return table

parse_file("story_module_select_info_table.data")


storyFiles = [name for name in os.listdir(fpath) if fnmatch(name,'story_module_story_info_table_*.data')]
sentences=[]
xx = []
for file in storyFiles:
    table = parse_file(file)
    df = pd.DataFrame(table)
    df = df.T    
    xx.append(df) 
    
    talk = []
    for sentences in table.values():
        senten = sentences['talk_content']
        # 替换掉女主的占位符
        senten = senten.replace('%NAME%','女主')
        man_talk[sentences['talk_name']].append(senten)
        talk.append(senten)
    # sentences.extend(list(talk))
    
# 保存中间结果
# da = pd.concat(xx)
# da.to_csv('fsfs.csv')



   


# # for x in sentences:
# #     if '长大' in x:
# #         print(x)

role = ['信长','光秀','秀吉']
pg,ax = plt.subplots(1,4)

for i,name in enumerate(role):
    talk = ''.join(man_talk[name])
    print('story length:',len(talk))
    wordcloud = WordCloud(font_path=r'D:\code\simfang.ttf').generate(jieba_processing_txt(talk))
    ax[i].imshow(wordcloud, interpolation='bilinear')
    ax[i].axis("off")
plt.show()


def getWordCloud(talk):
    return WordCloud(font_path=r'D:\code\simfang.ttf').generate(jieba_processing_txt(talk))

#%%


#%%
