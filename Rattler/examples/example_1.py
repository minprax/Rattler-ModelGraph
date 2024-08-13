import __init__
from base import base_functions, base_node, base_graph

def addxy(x, y): #The function that the node is actually going to perform
    return x+y

g = base_graph.Graph() #Create a graph



x_ = base_functions.Sink("x", int, value=1) #Creating the input variables, and giving some default values
y_ = base_functions.Sink("y", float, value=2)

z_ = base_functions.Source("z", float) #Creating the output variable, with no default value

function = base_functions.NodeFunction(addxy, x_, y_, z_) #Creating an NodeFunction object which associates the input/output
                                                           #variables with the actual function that is to be executed
                                                           #this only has to be created once for each identical node type

a1 = base_node.Node(title="A1")
a2 = base_node.Node(title="A2") #Creating 3 nodes
b1 = base_node.Node(title="B1")

a1.link_function(function)
a2.link_function(function) #Linking the above created NodeFunction object to each of the nodes
b1.link_function(function) #as they all do the same thing in this example

g.add_node(a1)
g.add_node(a2) #Adding the nodes to the Graph object
g.add_node(b1)

ed1 = base_graph.Edge(a1.var("z"), b1.var("x")) #Defining edges linking the outputs z from A1 and A2 to the inputs
ed2 = base_graph.Edge(a2.var("z"), b1.var("y")) #x and y of B1

g.add_edge(ed1) #Add the edges to the Graph object
g.add_edge(ed2)

print(a1)
print(a2) #Showing printout of the status of each node before graph execution
print(b1)

print("\n"*3, "="*5, "GRAPH EXECUTED", "="*5, "\n"*3)
g.run() #Execute the Graph

print(a1)
print(a2) #Showing printout of the status of each node after executing the graph
print(b1)





    
    
