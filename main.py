import string
from GraphGenerator import generate_graph_from_git_project, code_to_graph

projects = [
    "https://github.com/waz11/src1.git"
    # "https://github.com/waz11/AES.git",
    # "https://github.com/waz11/GUI_maze.git",
    # "https://github.com/Adarsh9616/Electricity_Billing_System.git",
    # "https://github.com/chabedalam11/Exam-Seating-Arrangement-System-Using-JSP-Servlet.git",
    # "https://github.com/meetakbari/CV-Resume-Builder.git"
]

def main():
    for project in projects:
        graphPath :string = generate_graph_from_git_project(project)

    # code_to_graph('./Files/codes/src1', 'Files/graphs/src1.json')


if __name__ == '__main__':
    main()

