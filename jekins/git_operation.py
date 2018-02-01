
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