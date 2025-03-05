from graphviz import Digraph

# Use Case Diagram
use_case = Digraph('UseCaseDiagram', format='png')
use_case.attr(rankdir='TB')
use_case.node('User', shape='stick figure')
use_case.node('System', shape='rectangle', label="Oratis System")

# Use Cases
use_case.node('UC1', 'Register & Login', shape='ellipse')
use_case.node('UC2', 'Start Interview', shape='ellipse')
use_case.node('UC3', 'Speech Recognition', shape='ellipse')
use_case.node('UC4', 'Non-Verbal Analysis', shape='ellipse')
use_case.node('UC5', 'Performance Feedback', shape='ellipse')

# Connections
use_case.edge('User', 'UC1')
use_case.edge('User', 'UC2')
use_case.edge('UC2', 'UC3')
use_case.edge('UC2', 'UC4')
use_case.edge('UC3', 'System')
use_case.edge('UC4', 'System')
use_case.edge('System', 'UC5')
use_case.edge('UC5', 'User')

# Render the diagram
use_case_path = "/images"
use_case.render(use_case_path)

use_case_path + ".png"
