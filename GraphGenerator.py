import os
import string
from git.repo.base import Repo
from Parser.CodeFromFile import CodeFromFile

# pip install gitpython

files_path= './Files'
codes_path = files_path+'/codes/'
graphs_path = files_path+'/graphs/'

def init_folders():
    for path in [files_path, codes_path, graphs_path]:
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)

def get_project_name(git_url):
    projectName = os.path.basename(git_url)
    projectName = projectName[0:projectName.rindex('.')]
    return projectName

def code_to_graph(codePath :string, outputPath :string) -> string:
    projectName: string = os.path.basename(codePath)
    CodeFromFile(codePath, projectName, outputPath)
    return outputPath

def clone_project_from_git(gitPath: string, outputPath :string) -> None:
    if not os.path.exists(outputPath):
        try:
            Repo.clone_from(gitPath, outputPath)
        except:
            print("git project hasn't found. try again.")


class GraphGenerator:

    def __init__(self):
        init_folders()

    def generate_graph_from_git_project(self, gitPath :string) ->string:
        project_name = get_project_name(gitPath)
        codePath = codes_path + project_name
        graphPath = graphs_path + project_name + '.json'

        if not os.path.exists(codePath):
            clone_project_from_git(gitPath, codePath)
            code_to_graph(codePath, graphPath)
        return graphPath

    def generate_graph_by_name(self, project_name :string) ->string:
        codePath = codes_path + project_name
        if not os.path.exists(codePath):
            print("project not found")
            return
        graphPath = graphs_path + project_name + '.json'
        code_to_graph(codePath, graphPath)
        return graphPath


