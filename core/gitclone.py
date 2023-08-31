# coding:utf-8


import sys

if sys.version_info < (3, 0):
    import urllib
else:
    from urllib.request import urlopen

import json
import subprocess, shlex
import time
import os


# gitlabAddr  = 'http://192.168.1.102'                 # gitlab 地址
# gitlabToken = 'glpat-DbJR6_faFoP3wx4QazY1'    # gitlab token

# clone_path = r"V:/PLE-Lib/extension/extend_maya/aaa"


def clone_project(git_project, gitlabAddr, gitlabToken, clone_path):
    for index in range(1, 10):
        url = "{}/api/v4/projects?private_token={}&per_page=100&page={}&order_by=name".format(gitlabAddr, gitlabToken, index)
        # print(url)

        if sys.version_info < (3, 0):
            allProjects = urllib.urlopen(url)
        else:
            allProjects = urlopen(url)

        allProjectsDict = json.loads(allProjects.read().decode(encoding='UTF-8'))

        for thisProject in allProjectsDict:
            if thisProject['name'] == git_project:
                try:
                    # thisProjectURL = thisProject['ssh_url_to_repo']
                    project_url = thisProject['http_url_to_repo']
                    project_path = os.path.join(clone_path, thisProject['name']).replace('\\', '/')
                    # print(project_path)

                    if os.path.exists(project_path):
                        command = shlex.split('git -C "{}" pull'.format(project_path))
                    else:
                        command = shlex.split('git clone {} {}'.format(project_url, project_path))

                    # subprocess.call(command)
                    process = subprocess.Popen(command)
                    process.wait()
                    time.sleep(0.5)

                except Exception as e:
                    raise e


# 克隆指定项目 
# clone_project('extend_maya')

