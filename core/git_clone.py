# coding:utf-8


import os
import gitlab


# GIT_URL = "http://192.168.1.102/"
# PRIVATE_TOKEN = "glpat-DbJR6_faFoP3wx4QazY1"
#
# PROJECT_NAME = "extend_blender"
# PROJECT_BRANCH = "main"
# DES_PATH = r"D:/test/git/extend_blender_v001"


class GitLab(object):
    def __init__(self, git_url: str, private_token: str):
        """
        :param git_url: gitLab地址(必传) example:"http://172.27.2.115/"
        :param private_token: gitlab 私有token (必传) example: "trTKyyyXK-y5CUrBkBzT"
        """
        self.git_url = git_url
        self.private_token = private_token
        self._check()

    def _check(self):
        if not self.git_url:
            raise Exception("请传入gitlab地址！")
        if not self.private_token:
            raise Exception("请传入private_token！")

    def _project_check(self, project_id, project_name, branch, to_path):
        if not branch:
            branch = "master"
            print("当前项目使用分支为master分支！")
        else:
            print(f"当前项目使用分支为{branch}分支！")
        if not project_name and not project_id:
            raise Exception("请传入项目ID或项目名称！")
        if not to_path:
            to_path = os.path.dirname(os.path.abspath(__file__))
            print(f"当前项目clone路径为: {to_path}")
        return project_id, project_name, branch, to_path

    def _get_project(self, project_id, project_name):
        self.git = gitlab.Gitlab(self.git_url, self.private_token)
        if project_id:
            return self.git.projects.get(project_id)
        if project_name:
            projects = self.git.projects.list()
            for project in projects:
                if project.name == project_name:
                    return project

    def _makedirs(self, dir_name):
        if not os.path.isdir(dir_name):
            print(f"创建目录: {dir_name}")
            os.makedirs(dir_name, exist_ok=True)

    def _get_full_path(self, to_path, origin):
        """获取目标路径"""
        return os.path.join(to_path, origin)

    def clone(self, project_id: int = None, project_name: str = None, branch: str = "master", to_path: str = None):
        """
        :param project_id: 项目Id
        :param project_name: 项目名称 (项目ID和项目名称必须传一个参数)
        :param branch: 分支名称 (默认master)  example: dev-gmj
        :param to_path: 克隆地址(如果不传该参数，默认在当前文件目录路径)
        :return:
        """
        project_id, project_name, branch, to_path = self._project_check(project_id, project_name, branch, to_path)
        project = self._get_project(project_id, project_name)
        repository_tree = project.repository_tree(all=True, ref=branch, recursive=True, iterator=True)
        for item in repository_tree:
            if item['type'] == "tree":
                self._makedirs(self._get_full_path(to_path, item['path']))
            else:
                file = project.files.get(file_path=item['path'], ref=branch)
                print(f"下载文件: {item['path']} ")
                with open(self._get_full_path(to_path, item['path']), 'wb') as fw:
                    fw.write(file.decode())
                print(f"下载完成: {item['path']} ")


# if __name__ == '__main__':
#     git = GitLab(GIT_URL, PRIVATE_TOKEN)
#     git.clone(project_id=PROJECT_ID, branch=PROJECT_BRANCH, to_path=DES_PATH)
#     git.clone(project_name=PROJECT_NAME, branch=PROJECT_BRANCH, to_path=DES_PATH)


