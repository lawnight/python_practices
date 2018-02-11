# -*- coding: utf-8 -*-
# 本地打包脚本
import os
import shutil
import re
import time

from distutils.dir_util import copy_tree

force_update = False
update_branch = 'develop'
commit_branch = 'develop'

excelPath = r'G:\100day\for_pack\loui_cn_excel'

to_excelPath = r'G:\100day\loui_pack\loui_cn_server\gameSrv\excel'


game_server_path = r'G:\100day\for_pack\loui_cn_server'
to_gamePath = r'G:\100day\loui_pack\loui_cn_server\gameSrv'

def push(path):
    os.chdir(path)
    os.system('git push')

def pull(path, branch):
    os.chdir(path)
    os.system('git checkout %s' % branch)

    p = os.popen('git pull')
    result = p.read()
    #print (result)
    flage = True
    if 'Already up-to-date' in result and not force_update:
        flage = False

    # get commit hash
    p = os.popen('git log')
    version = re.search('commit (.*)\\n?', p.read()).group(1)
    return flage, version, result


def commit(path, msg):
    os.chdir(path)
    os.system('git checkout %s' % commit_branch)
    os.system('git add .')
    os.system('git commit -m "%s"' % msg)


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
            shutil.copy2(s, d)

        # os.chdir(r'G:\100day\brgz_cn_server')
        # p=os.popen("git checkout princess-develop")


def compile(path):
    os.chdir(path)
    os.system('mvn clean')
    os.system('mvn -Dmaven.test.skip=true package')


def copy(subDir):
    src = os.path.join(game_server_path, 'target', subDir)
    dst = os.path.join(to_gamePath, subDir)
    if '.jar' in subDir:
        shutil.copy2(src, dst)
    else:
        copytree(src, dst, ignore={'.git'})


def process_excle():

    print '--------processing excel start'
    flage, version, result = pull(excelPath, update_branch)
    
    # pull(to_excelPath,commit_branch)
    print '--------copy to'
    copytree(excelPath, to_excelPath, ignore={'.git'})
    commit(to_excelPath, "excel develop branch SHA-1:%s" % version)
    push(to_excelPath)
    print '--------processing excel end'


def process_server():
    print '--------processing server'
    flage, version, result = pull(game_server_path, update_branch)


    if flage:
        compile(game_server_path)
        # copy('lib')
        # copy('resources')
        copy('princess-server.jar')
        commit(to_gamePath, "server develop branch SHA-1:%s" % version)
        print '--------processing server end'
    else:
        print '--------processing server end nothing chage'


process_excle()
process_server()
