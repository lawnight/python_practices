
# 讲大数据字段说明.xml 生成java对应的类
from lxml import etree

obj = etree.parse(r'/Users/near/Downloads/log (2).xml')

root = obj.getroot()

tables = {}

typeMap = {'string':'String',
           'bigint':'long',
           }

filter_name = ['AppID','GameID','ChildId','IP','LogTime','CharacterID','LogType','AccountID']

for i,v in enumerate(root):
    if v.tag == 'struct':
        if  v.attrib['name']:
            name = v.attrib['name']
            des = v.attrib['desc']
            table = []
            for j in v:
                table.append(j.attrib)
            tables[(name,des)] = table

text = ''
with open('/Users/near/code/python_practices/bigdata.tpl') as f:
    text = f.read()

# 生成文件
for k,v in tables.items():
    data = text.replace('$class',k[0])
    data = data.replace('$des',k[1])
    x = ''
    c = 1
    # 生成字段
    names = []
    for i,field in enumerate(v):

        t = field['type']
        if t in typeMap:
            t = typeMap[t]
        name = field['name']

        name = name[0].lower() + name[1::]
        name = name.replace('eX1','ex1')
        name = name.replace('eX2','ex2')
        name = name.replace('eX3','ex3')
        name = name.replace('eX4','ex4')
        name = name.replace('appID','appId')
        name = name.replace('gameID','gameId')
        name = name.replace('accountID','accountId')
        name = name.replace('characterID','playerId')
        name = name.replace('logType','NAME')
        name = name.replace('iP','ip')
        name = name.replace('serverID','serverId')

        names.append(name)
        if field['name'] not in filter_name:
            x += '\n    /** {} */\n'.format(field['desc'])
            x += '    private String {} = StringConstants.EMPTY;'.format(name)

    data = data.replace('$fields_fcc',x)
    # $fields_format
    data = data.replace('$fields_format', '|'.join(['{}']*len(names)))
    # $fields_com

    data = data.replace('$fields_com', ','.join(names))
    # print(data)
    with open('/Users/near/work/war_mix_server/server/src/main/java/com/digisky/gal/warstates/gameserver/bigdata/logs/'+k[0] + 'Log.java','w') as f:
        f.write(data)