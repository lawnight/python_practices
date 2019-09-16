import pandas as pd

data = pd.read_csv(r'C:\Users\Dell\Downloads\DuplicateInfo1564650201341.csv',encoding='gbk')
# 不要gm打过的关卡
data = data[(data['通关点数']!=99999999) & (data['战斗类型0系统活动1普通关卡2精英关卡3运营活动']==1)]

aIds = ['3-2','3-15','5-2','5-16','6-1','6-15','8-2','8-14','9-1','9-15','11-1','11-15','12-2','12-15','13-1','13-13']
bIds = ['2-5','2-15','4-3','4-15','5-6','5-19','7-3','7-17','8-5','8-18','10-2','10-17','11-5','11-19','13-6','13-9']

a = pd.ExcelFile(r'D:\code\war_mix_server\excel\read\SectionConfig.xlsx')
section = a.parse(a.sheet_names[0])
#g = section['玩法关ID'].groupby(section['本话名称(地图显示）'])

# playId得到
def playId(ids):
    for sId in ids:
        selected = section[(section['话分类']=='PLAY') & (section['本话名称(地图显示）'] == sId)]
        b = selected['玩法关ID']
        c = eval(b.iloc[0])
        playerId = c[0]
        yield playerId

bb = list(playId(bIds))

# for name,group in :
#     if name in bb:
#         left = group['通关时间：']
#         print(type(group))
#         #print(name,max(left),min(left),count(group))
c1 = '通关时间：'
data[c1] = pd.to_numeric(data[c1].str[0:-1])
filter = data[data['副本ID'].isin(bb)]
group =filter.groupby(['副本ID'])

group['通关时间：'].agg(['min','max','size'])