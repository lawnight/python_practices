# -*- coding: utf-8 -*-
# jekins更新到外测所用的脚步
import os
import re
import shutil
from subprocess import call
import subprocess


def pull(path, branch):
    os.chdir(path)
    os.system('git checkout %s' % branch)
    
    p = os.popen('git pull')
    result = p.read()
    #print (result)
    if 'Already up-to-date' in result:
        return False, 0, result

    # get commit hash
    p = os.popen('git log')
    version = re.search('commit (.*)\\n?', p.read()).group(1)
    return True, version, result


def commit(path,commit_branch ,msg): 
    os.chdir(path)
    os.system('git checkout %s' % commit_branch)
    os.system('git add .')
    os.system('git commit -m %s' % msg)

        
def get_version(path,branch):
    os.chdir(path)
    p = os.popen('git log')
    version = re.search('commit (.*)\\n?', p.read()).group(1)
    return version

def push(path):
    os.chdir(path)
    os.system('git push')


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            if '.git' not in s:
                copytree(s, d, symlinks, ignore)
        else:
            # if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
            if '.git' not in s:
                shutil.copy2(s, d)

#cpy excel
src_excel =  r'/root/jenkins/workspace/陆版百日_更新配置'
to_path = r'/root/jenkins/repository/brgz_cn_server/gameSrv/'


src_code = r'/root/jenkins/workspace/陆版百日_重新打包_重启服'
to_code = r'/root/jenkins/repository/brgz_cn_server/gameSrv'


#cpy excel
excelPath = os.path.join(to_path,'excel')
copytree(src_excel,excelPath)
version = get_version(src_excel,'develop')
print 'excel version is:' + version
commit(excelPath,'princess-develop','excel:%s' % version)



#cpy princess.lib
shutil.copy2('/root/jenkins/workspace/陆版百日_重新打包_重启服/target/princess-server.jar',os.path.join(to_path,'princess-server.jar'))
#cpy lib
copytree('/root/jenkins/workspace/陆版百日_重新打包_重启服/target/lib',os.path.join(to_path,'lib'))
#cpy server
version = get_version(src_code,'develop')
commit(to_code,'princess-develop','server:%s' % version)


push(to_code)



