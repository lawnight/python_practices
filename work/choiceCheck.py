"""
检查客服端和服务器 choice的配置
"""
#%%
import pandas  as pd
import os
from collections import defaultdict
import xxtea
import json
import numpy as np

key = 'jgbw2eu3fhk4sb5g'

path = r'D:\code\war_mix_server\excel\read'

t = pd.read_excel(os.path.join(path,"ChoiceConfig.xlsx"))    
# 过滤
t = t[3::]
t = t[t['ChoiceConfig']!='###']
read_choice = t[t['小节分类'] == 'READ']
topic_choice = t[t['小节分类'] == 'TOPIC']
#t = t[['选择ID', '所属小节(话)ID']]



def decodeFile(story_path):    
    with open(story_path,'rb') as f:
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
        #df.to_csv(os.path.join(fpath,story_path+'.csv'))
        return df

# 选项index表
# f = decodeFile(os.path.join(r'D:\code\war_mix_server\client\Documents\reading_story','story_module_select_info_table.data'))
# f.index = pd.to_numeric(f.index)


# def getChoiceByStroyId(storyId):
#     path = r'D:\code\war_mix_server\client\Documents\reading_story'
#     t = decodeFile(os.path.join(path,'story_module_story_info_table_{}.data'.format(storyId)))
#     # file = os.path.join(path,'story_module_story_info_table_{}.data.csv'.format(storyId))
#     # print('read',file)
#     # t = pd.read_csv(file)
    
#     c =  t['select_info_ids']
#     c = c.replace('',np.nan)
#     c = c.dropna()
#     choices = defaultdict(list)

#     if not c.empty:
#         for i,choice in enumerate(c,1):
#             choice_index = choice.split('|')
#             data = []
#             #print('转换选项id',choice,storyId)
#             for index in choice_index:
#                 choice = f.iloc[int(index)-1]['value']  
#                 data.append(choice)    
#             choices[i] = data
#     return choices

#%%
t = pd.read_excel(os.path.join(path,"ChoiceSettingForStoryModule.xlsx"))    
# 过滤
t = t[3::]
t = t[t['ChoiceSettingNew']!='###']
#t = t[t['小节分类'] == 'READ']
#t = t[['选择ID', '所属小节(话)ID']]
client_choice = t


def getChoiceByStroyId(storyId):
    """
        通过剧本id得到选项
    """
    x = client_choice[client_choice['所属小节(话)ID']==storyId]
    #x = x.dropna()
    choices = defaultdict(list)

    for g,item in x.groupby('选项组别序号'):
        for i in item['选择ID']:
            choices[g].append(i)
    return choices

#print(getChoiceByStroyId(100046))

#%%
def applyItem(x):
    #print(type(x),x.index)
    storyId = x['剧本']  
    sectionId = x['小节ID']  

    choices = getChoiceByStroyId(storyId)
    if len(choices)>0:
        #print('check choice',sectionId,choices)
        choiceConfig(sectionId,choices)



# for row in t.iterrows():
#     sId, = row
#     for item in c.iterrows():
#         print('choice',item)
count = 0

def choiceConfig(sectionId,choice,topic = False):
    global read_choice
    global topic_choice
    global count
    if topic:
        t = topic_choice[topic_choice['所属小节(话)ID']==sectionId]
    else:
        t = read_choice[read_choice['所属小节(话)ID']==sectionId]
    for groupId,grouped in t.groupby('选项组别序号'):
        ids = choice[groupId]
        ids = [int(x) for x in ids]
        ids2 = [int(x) for x in list(grouped['选择ID'])]
        ids.sort()
        ids2.sort()
        if ids ==ids2 :
            #print('选项相等',ids,ids2,'sectionId',sectionId)            
            pass
        else:
            context ='sectionId'
            if topic:
                context = "topicId"
            print('选项配置和客服端不一致 <{} -- {}> {}:{}'.format(ids,ids2,context,sectionId))
            count = count +1
            




t = pd.read_excel(os.path.join(path,"SectionConfig.xlsx"),sheet_name='话配置')
t = t[t['SectionConfig']!='###']
t = t[['小节ID', '剧本']]
t = t[3::]
t = t.dropna()
section_table = t

def readGameExcel(path):
    t = pd.read_excel(path)
    t = t[3::]
    t = t[t.iloc[:,0]!='###']
    return t


# 开始处理
print("检查section的话选项")
section_table.apply(applyItem,axis=1)
print("检查topic的话选项")
for r,d,fs in os.walk(r'D:\code\war_mix_server\excel\topicStory\story_data'):
    for f in fs:
        try:
            topicId = f[12:-5]
            if '~' in f:
                continue
            x = readGameExcel(os.path.join(r,f))

            b1 = x['触摸后对应增加数值']
            b1 = b1.replace('',np.nan)
            b1 = b1.dropna()

            x = x['对应增加参数']
            x = x.replace('',np.nan)
            x = x.dropna()
            choices = defaultdict(list)
            for i,j in enumerate(b1,1):
                choices[i] = str(j).split(',')
            for i,j in enumerate(x,1):
                choices[i] = str(j).split(',')
            # if len(choices)>0:
            #print('check topic',topicId,choices)
            choiceConfig(topicId,choices,True)
        except Exception as e:
            print(e)

print('检查完毕 有{}处错误'.format(count))

#%%
