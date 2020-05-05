# 改名的程序，
import os
path = r'D:\电影\死亡笔记\死亡笔记动漫'
# Step 1：定义如何改名
def changeName(old):
    #new = old[5:-1]
    new = old + 'b'
    return new
os.chdir(path)
for files in os.listdir():
    old = os.path.join(path,files)
    print(files)
    new = changeName(files)
    print(new)
    # Step 2:先注释下面改名的代码，等测试通过再打开
    os.rename(old,os.path.join(path,new))