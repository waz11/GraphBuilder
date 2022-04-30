import os
import string
from git.repo.base import Repo
from Parser.CodeFromFile import CodeFromFile

# pip install gitpython


def generate_path_to_code(pathToCode :string) -> string:
    if 'git' in pathToCode:
        projectName = os.path.basename(pathToCode)
        projectName = projectName[0:projectName.rindex('.')]
        sourcePath: string = 'Files/codes/' + projectName
        return sourcePath
    else: return pathToCode

def generate_path_to_graph(pathToCode :string) -> string:
    projectName: string = os.path.basename(pathToCode)
    outputPath = 'Files/graphs/' + projectName + '.json'
    return outputPath

def generate_graph_from_git_project(gitPath: string) -> string:
    codePath = generate_path_to_code(gitPath)
    graphPath = generate_path_to_graph(codePath)
    if not os.path.exists(codePath):
        clone_project_from_git(gitPath, codePath)
    # if not os.path.exists(graphPath):
    code_to_graph(codePath, graphPath)
    return graphPath


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