import string
from GraphGenerator import generate_graph

projects = [
    "https://github.com/waz11/AES.git",
    # "https://github.com/waz11/GUI_maze.git",
    # "https://github.com/Adarsh9616/Electricity_Billing_System.git",
    # "https://github.com/chabedalam11/Exam-Seating-Arrangement-System-Using-JSP-Servlet.git",
    # "https://github.com/meetakbari/CV-Resume-Builder.git"
]

def main():
    for project in projects:
        graphPath :string = generate_graph(project)


if __name__ == '__main__':
    main()

