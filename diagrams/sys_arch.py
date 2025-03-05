# System Architecture Diagram
architecture = Digraph('SystemArchitecture', format='png')
architecture.attr(rankdir='TB', style='filled', color='lightgrey')

# Components
architecture.node('User', shape='parallelogram', style='filled', color='lightblue')
architecture.node('Frontend', 'React Frontend', shape='box', style='filled', color='lightyellow')
architecture.node('Backend', 'Python Backend (FastAPI)', shape='box', style='filled', color='lightyellow')
architecture.node('AI_Model', 'AI Processing (Speech & NLP Models)', shape='box', style='filled', color='lightgreen')
architecture.node('DB', 'Database (PostgreSQL)', shape='cylinder', style='filled', color='lightpink')

# Connections
architecture.edge('User', 'Frontend', label='Access via Web Browser')
architecture.edge('Frontend', 'Backend', label='API Calls (REST)')
architecture.edge('Backend', 'AI_Model', label='Process Speech & NLP')
architecture.edge('Backend', 'DB', label='Store & Retrieve Data')

# Render the diagram
architecture_path = "/mnt/data/system_architecture"
architecture.render(architecture_path)

architecture_path + ".png"
