# 检查客服端和服务器 choice的配置
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
t = t[4::]
t = t[t['ChoiceConfig']!='###']
t = t[t['小节分类'] == 'READ']
#t = t[['选择ID', '所属小节(话)ID']]
read_choice = t



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
f = decodeFile(os.path.join(r'D:\code\war_mix_server\client\Documents\reading_story','story_module_select_info_table.data'))
f.index = pd.to_numeric(f.index)
f = f.replace('',np.nan)
f = f.dropna()


def getChoiceByStroyId(storyId):
    path = r'D:\code\war_mix_server\client\Documents\reading_story'
    t = decodeFile(os.path.join(path,'story_module_story_info_table_{}.data'.format(storyId)))
    # file = os.path.join(path,'story_module_story_info_table_{}.data.csv'.format(storyId))
    # print('read',file)
    # t = pd.read_csv(file)
    
    c =  t['select_info_ids']
    choices = defaultdict(list)

    if not c.empty:
        for i,choice in enumerate(c,1):
            choice_index = choice.split('|')
            data = []
            for index in choice_index:
                choice = f.iloc[int(index)]['value']  
                data.append(choice)    
            choices[i] = data
    return choices

#%%
def applyItem(x):
    #print(type(x),x.index)
    storyId = x['剧本']  
    sectionId = x['小节ID']  

    choices = getChoiceByStroyId(storyId)
    print('check choice',sectionId,choices)
    choiceConfig(sectionId,choices)



# for row in t.iterrows():
#     sId, = row

#     for item in c.iterrows():
#         print('choice',item)
    

def choiceConfig(sectionId,choice):
    global read_choice
    t = read_choice[read_choice['所属小节(话)ID']==sectionId]
    for groupId,grouped in t.groupby('选项组别序号'):
        ids = choice[groupId]
        ids2 = list(grouped['选择ID'])
        ids.sort()
        ids2.sort()
        if ids ==ids2 :
            print('选项相等',sectionId,ids,ids2)
        else:
            print('选项不等',sectionId,ids,ids2)


# x = pd.merge(t1,t,left_on='剧本',right_on='所属小节(话)ID',how='right')

# x.drop(['所属小节(话)ID','剧本'],axis=1)

# file = pd.ExcelFile(os.path.join(path,"ChoiceConfig.xlsx"))
# t = file.parse('选择表')
# t = t[3::]

# x = pd.merge(x,t,left_on='选择ID',right_on='选择ID',how='outer',indicator=True)
# x['_merge'].value_counts()


t = pd.read_excel(os.path.join(path,"SectionConfig.xlsx"),sheet_name='话配置')
t = t[t['SectionConfig']!='###']
t = t[['小节ID', '剧本']]
t = t[3::]
t = t.dropna()
section_table = t

# 开始处理
section_table.apply(applyItem,axis=1)

#%%
