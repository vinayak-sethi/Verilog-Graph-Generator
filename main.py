#Author: Vinayak Sethi

# A function that print all paths between thw source and destination
def printAllPaths(graph1, source, destination, visited1, path1):
    visited1[source] = True
    path1.append(source)  # Append the source to the path
    if source == destination: # If the source and destination is reached, the path is complete
        print(path1) # Append the path to the output
    else: # If the source is different to the destination
        for it in graph1[source]: # Loop through the list of next nodes
            if not visited1[it]: # If the node in not visited
                printAllPaths(graph1, it, destination, visited1, path1)  # Update the source with the same destination
    path1.pop() # If the source does not match the destination or all its children are visited, pop the latest node
    visited1[source] = False

#Main Function
if __name__ == '__main__':
    filePath = input("\nEnter the path of the file: ")

    graph = {} # Instantiate the graph dictionary
    input_gate = {} 
    not_gate = {}
    data = { #Instantiate the dictionary for different data types
        'input': [],
        'output': [],
        'wire': []
    }
    # There can be three types of data => input, output, wire
    # Reg cannot have continuous assignment, so it is excluded
    input_data_type = ['input', 'output', 'wire']
    input_gate_type = ['and', 'nand', 'or', 'nor', 'xor', 'xnor', 'not']

    with open(filePath, "r") as fp: # Open the .v file taken from the user in read mode
        fileData = fp.readlines() #Iterate over each lines

    for it in fileData: # Loop through each line
        # Separate the variables from the symbols
        it = it.replace(',', ' , ')
        it = it.replace(';', ' ; ')
        it = it.replace('(', ' ( ')
        it = it.replace(')', ' ) ')
        # Split each line into words
        name = it.split()
        if len(name) == 0: # If the line is empty
            continue # Goto the next line
        if name[0] == 'module' or name[0] == 'endmodule': # If the line has the keywords 'module' and 'endmodule'
            continue # Goto the next line
        elif name[0] in input_data_type: # If the line starts with a input data type
            for a in name: # Loop through the words of that line
                if a != ',' and a != ';' and a != name[0]: # Ignore the data type and the symbols => ',' and ';'
                    data[name[0]].append(a) # Append the variables to the data
        else:
            gate = name[0] # Get the gate name
            gate_name = name[1] # Get the instantiation name of the gate
            if gate == 'not':
                not_gate[gate_name] = [] # Add the gate instantiation name to the dictionary
            else:
                input_gate[gate_name] = [] # Add the gate instantiation name to the dictionary
            name = name[2:] # Ignore the first two words
            if gate in input_gate_type: # If the word is a gate
                for a in name: # Loop through the words of that line
                    if a != '(' and a != ')' and a != ',' and a != ';': # Ignore the symbols => '(', ')', ',', ';'
                        if gate == 'not': 
                            not_gate[gate_name].append(a) # Add to the not gate dictionary
                        else:
                            input_gate[gate_name].append(a) # Add to the other gates dictionary

    for i in data['input']:  # Add the inputs to the graph as nodes
        graph[i] = []
    for i in input_gate.keys(): # Add the gates to the graph as nodes
        graph[i] = []
    for i in not_gate.keys(): # Add the not gates to the graph as nodes
        graph[i] = []
    for i in data['output']: # Add the outputs to the graph as nodes
        graph[i] = []
    for i, j in not_gate.items(): # Loop through not gates
        # not not_0 (out, in)
        # If 'in' is an input
        if j[1] in data['input']:
            graph[j[1]].append(i) # Append the gate to the input
        else: # If 'in' is a wire
            for k, l in not_gate.items(): # Loop through the not gates
                if l[0] == j[1]: # If the output of the other gate is the input of the present gate
                    graph[k].append(i) # Append the gate to the present gate
            for k, l in input_gate.items(): # Loop through the other gates
                if l[0] == j[1]:  # If the output of the other gate is the input of the present gate
                    graph[k].append(i) # Append the gate to the present gate
        
        if j[0] in data['output']: # If 'out' is an output
            graph[i].append(j[0]) # Append the output to the present gate
    for i, j in input_gate.items(): # Loop through the other gates
        # gate gate_0 (out, in1, in2)
        # If 'in1' is an input
        if j[1] in data['input']:
            graph[j[1]].append(i) # Append the gate to the input
        if j[2] in data['input']: # If 'in2' is an input
            graph[j[2]].append(i) # Append the gate to the input
        if j[1] in data['wire']: # If 'in1' is a wire
            for x, y in input_gate.items(): # Loop through the other gates
                if y[0] == j[1]: # If the output of the other gate is the input of the present gate
                    graph[x].append(i) # Append the gate to the present gate
            for x, y in not_gate.items(): # Loop through the not gates
                if y[0] == j[1]: # If the output of the other gate is the input of the present gate
                    graph[x].append(i) # Append the gate to the present gate
        if j[2] in data['wire']: # If 'in1' is a wire
            for x, y in input_gate.items(): # Loop through the other gates
                if y[0] == j[2]: # If the output of the other gate is the input of the present gate
                    graph[x].append(i) # Append the gate to the present gate
            for x, y in not_gate.items(): # Loop through the not gates
                if y[0] == j[2]: # If the output of the other gate is the input of the present gate
                    graph[x].append(i) # Append the gate to the present gate
        if j[0] in data['output']: # If 'out' is an output
            graph[i].append(j[0]) # Append the output to the present gate

    # Create a dictionary of the nodes for finding the paths
    temp = list(input_gate.keys()) + data['input'] + data['output'] + list(not_gate.keys())
    visited = {}
    for i in temp: # Initialize visited of all nodes to false
        visited[i] = False
    path = [] # Initialize an empty path
    
    # For each combination of input and output
    print('\nAll the paths from Input to Output are :\n')
    for i in data['input']:
        for j in data['output']:
            printAllPaths(graph, i, j, visited, path) # Find all paths between them
        