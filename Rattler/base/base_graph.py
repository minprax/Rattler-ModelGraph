from random import randrange #For generating object id numbers
import copy

from . import CustomErrors


class Edge():
    """
    Connections between nodes.

    Attributes
    ----------
        fromPort : FunctionVariable
            The output variable object of the past node.
        toPort : FunctionVariable
            The input variable object of the next node.
        fromNode : Node
            Node object that owns the fromPort.
        toNode : Node
            Node object that owns the toPort.
        id : int
            A random number to avoid name confusion.
    """
    def __init__(self, fromPort, toPort):
        """
        Constructs attributes for each edge.

        Parameters
        ----------
            fromPort : FunctionVariable
                The output variable object (Source) of the past node.
            toPort : FunctionVariable
                The input variable object (Sink) of the next node.
        """
        self.fromPort = fromPort
        self.toPort = toPort

        self.fromNode = self.fromPort.ofNode.id
        self.toNode = self.toPort.ofNode.id

        self.id = randrange(1, 9999999999)


class Graph():
    """
    The object to contain all internal information on a graph.

    Attributes
    ----------
        node_list : dict
            A dictionary of nodes in the graph, keyword is the node id.
        edge_list : dict
            A dictionary of edges in the graph, keyword is the edge id.

    Methods
    -------
        add_node(node)
            Add a node to the graph.
        del_node_byid(node_id)
            Delete a node  from the graph by its id number. Does not delete the node object.
        del_node_byobj(this_node)
            Delete a node from the graph by its object. Does not delete the node object.
        add_edge(edge)
            Add an edge object to the graph.
        del_edgebyid(edge_id)
            Delete an edge from the graph using its id number. Does not delete the edge object.
        del_edgebyobj(this_edge)
            Delete and edge from the graph using it sobject. does not delete the edge object.
        order_nodes()
            Sorts the nodes in the graph into an execution order according to Kahn's algorithm for topological sorting. 
    """
    def __init__(self):
        """
        Constructs initial attributes for the instance.
        """
        self.node_list = {}
        self.edge_list = {}

    def add_node(self, node):
        """
        Add a node to the graph.

        Parameters
        ----------
            node : Node
                An instance of the Node class.
        """
        self.node_list[node.id] = node

    def del_node_byid(self, node_id):
        """
        Delete a node from the graph by its id number. Does not delete the node object.

        Parameters
        ----------
            node_id : int
                Id number of the node to delete.
        """
        del self.node_list[node_id]

    def del_node_byobj(self, this_node):
        """
        Delete a node from the graph by its object. Does not delete the node object.

        Parameters
        ----------
            this_node : Node
                An instance of the Node object, the one to delete.
        """
        del self.node_list[this_node.id]

    def add_edge(self, edge):
        """
        Add an edge object to the graph.

        Parameters
        ----------
            edge : Edge
                An instance of the Edge class between two variables/nodes.
        """
        self.edge_list[edge.id] = edge

    def del_edgebyid(self, edge_id):
        """
        Delete an edge from the graph using its id number. Does not delete the edge object.

        Parameters
        ----------
            edge_id : int
                The edge id number.
            
        """
        del self.edge_list[edge_id]

    def del_edgebyobj(self, this_edge):
        """
        Delete an edge from the graph using its id number. Does not delete the edge object.

        Parameters
        ----------
            edge_id : int
                The edge id number.
            
        """
        del self.edge_list[this_edge.id]

    def run(self):
        """
        Execute nodes in the correct order.
        """
        for node in self.order_nodes():
            edges_to_n = [edge for edge in self.edge_list.values() if edge.toNode is node] #Constuct the list of edges to pull input vars from
            self.node_list[node].run(edges_to_exec = edges_to_n)

    def order_nodes(self):
        """
        Sorts the nodes in the graph into an execution order according to Kahn's algorithm for topological sorting.

        Returns
        -------
            list : ints
                Node ids in a list in order they should be executed.
        """
        if len(self.edge_list) == 0 or len(self.node_list) == 0: #Verify a valid graph has been created
            raise CustomErrors.EmptyNetwork
        
        nodes_with_parent = [edge.toNode for edge in self.edge_list.values()]
        nodes_no_parents = [node_id for node_id in self.node_list if node_id not in nodes_with_parent] #Create the starting sets to itterate over
        ordered = []
        remaining_edges = copy.deepcopy(self.edge_list) #Copy to avoid modification to the edge_list while itterating
        
        while len(nodes_no_parents) > 0:
            n = nodes_no_parents[0]
            del nodes_no_parents[0] #Nodes with no remaining parents can be imediatly added to the ordered list
            ordered.append(n)

            #Create a list of children of the most recently added node            
            n_goes_to = [(edge, remaining_edges[edge].toNode) for edge in remaining_edges if remaining_edges[edge].fromNode == n]
            
            for e, m in n_goes_to:
                del remaining_edges[e] #Remove edges from last node added to ordered list, to next node under inspection
                
                m_goes_to = [1 for edge in remaining_edges if remaining_edges[edge].toNode == m] #If the node under inspection still now has no parents
                if len(m_goes_to) == 0:                                                            #then its parents are all in the ordered list already
                    nodes_no_parents.append(m)                                                      #and it can be safely executed (hence added to ordered)
                    
        if len(remaining_edges) > 0:
            raise CustomErrors.CircularReference
        else:
            return ordered
                    
