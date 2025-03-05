# Sequence Diagram
sequence = Digraph('SequenceDiagram', format='png')
sequence.attr(rankdir='TB', style='filled', color='lightgrey')

# Entities
sequence.node('User', 'User', shape='parallelogram', style='filled', color='lightblue')
sequence.node('Frontend', 'React Frontend', shape='box', style='filled', color='lightyellow')
sequence.node('Backend', 'Python Backend', shape='box', style='filled', color='lightyellow')
sequence.node('AI', 'AI Processing', shape='box', style='filled', color='lightgreen')
sequence.node('DB', 'Database', shape='cylinder', style='filled', color='lightpink')

# Sequence Interactions
sequence.edge('User', 'Frontend', label='Login/Register')
sequence.edge('Frontend', 'Backend', label='API Request: Authenticate User')
sequence.edge('Backend', 'DB', label='Query: Validate Credentials')
sequence.edge('DB', 'Backend', label='Return: Authentication Result')
sequence.edge('Backend', 'Frontend', label='Response: Success/Fail')

sequence.edge('User', 'Frontend', label='Start Interview')
sequence.edge('Frontend', 'Backend', label='API Request: Start Simulation')
sequence.edge('Backend', 'AI', label='Send Speech & Video Data')
sequence.edge('AI', 'Backend', label='Return Processed Analysis')
sequence.edge('Backend', 'DB', label='Store Performance Data')
sequence.edge('Backend', 'Frontend', label='Return Performance Metrics')
sequence.edge('Frontend', 'User', label='Display Feedback')

# Render the diagram
sequence_path = "/mnt/data/sequence_diagram"
sequence.render(sequence_path)

sequence_path + ".png"
