
# 检查对应关系


a = """<metalib tagsetversion="1" name="Log" version="1.1">
    <!-- 以下由服务器采集 -->
    <struct name="AccountRegister" version="1" desc="注册信息 ">
        <entry name="AppID" type="string" size="50"  desc="(必填)应用ID"/>
        <entry name="GameID" type="string" size="32"  desc="(必填)游戏ID"/>
        <entry name="ChildId" type="string" size="32"  desc="(必填)子版本ID"/>
        <entry name="IP" type="string" size="20"  desc="(必填)登陆IP"/>
        <entry name="AccountID" type="string" size="50"  desc="(必填)账号ID"/>
        <entry name="LogType" type="string" size="20" default="AccountRegister" desc="(必填)日志类型 固定值"/>
        <entry name="LogTime" type="bigint" size="13"  desc="(必填)日志时间 单位毫秒"/>
        <entry name="PlatformChannelId" type="string" size="100"  desc="(可选)渠道平台ID"/>
        <entry name="Idfa" type="string" size="35" desc="(必填)IOS广告标示符"/>
        <entry name="Android_id" type="string" size="35" desc="(必填)安卓标示符"/>
        <entry name="Mac" type="string" size="18" desc="（必填）MAC地址 格式：00edfsc00001，去掉字母小写，去掉'-'或'：'"/>
    </struct>
</metalib>"""

def getTheChild(name):
    for child in root2.getchildren():
        if child.tag== 'struct':
            if child.get('name') == name:
                return child

from lxml import etree

p = r'C:\Users\Dell\Downloads\log.xml'

with open(p, 'r', encoding='utf8') as f:
    str = f.read()
    root2 = etree.fromstring(str)

root = etree.fromstring(a)
for child in root.getchildren():
    if child.tag == 'struct':
        print("## " + child.get('desc').replace(r'（必填）', ''))
        print("")
        names = []
        values = []  # 原始定义
        values2 = []  # 自己定义的
        ar = "AppID	GameID	ChildId	IP	ServerID	AccountID	CharacterID	LogType	LogTime	PlatformChannelId".split(
            "\t")

        child2 = getTheChild(child.get('name'))
        for sub,sub2 in zip(child.getchildren(),child2.getchildren()):
            name = sub.get('name')
            if name not in ar:
                value = sub.get('desc')
                value = value.replace("(必填)", "")
                value = value.replace("(可选)", "")
                names.append(name)


                value2 = sub2.get('desc')
                value2 = value2.replace("(必填)", "")
                value2 = value2.replace("(可选)", "")
                values.append(value2)
                if value2 == value:
                    values2.append("")
                else:
                    values2.append(value)
        print(r'<div class="datatable-begin"></div>')
        print("")
        print("表头" + "|" + "|".join(values))
        print('|'.join(["----"] * (len(names) + 2)))
        print("**字段名**|" + "|".join(names) )
        print("**补充说明**|" + "|".join(values2) )
        print("")
        print(r'<div class="datatable-end"></div>')
        print("")



