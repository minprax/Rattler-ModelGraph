from random import randrange #For generating object id numbers
import copy

class Node:
    """Base class for nodes.

    Attributes
    ----------
        title : str
            Name of the node visible to users.
        linked_func : NodeFunction
            The function and variable container bound to the node instance.
        id : int
            A random id number to avoid name confusion.

    Methods
    -------
        run(edges_to_exec = [])
            Execute the node.
        var(variable=None)
            Return a variable of function bound to the node.
        link_function(linked_func)
            Bind a function, defined in the implementation, to this node instance.
    """
    def __init__(self, title = "Untitled", linked_func = None):
        """
        Constructs attributes for node, and attempts to bind a linked function.

            Parameters
            ----------
            title : str, optional
                Name of the node visible to users.
            linked_func : NodeFunction, optional
                Container class for the variables and function to call for the node instance.
        """
        self.title = title
        self.linked_func = None

        self.id = randrange(1, 9999999999)

        if linked_func:
            self.link_function(self.linked_func)

    def run(self, edges_to_exec = []):
        """
        Execute the node

        Parameters
        ----------
            edges_to_exec : [Edge], optional
                List of edges that terminate at this node.
        """
        self.linked_func.run(edges_to_exec)

    def var(self, variable):
        """
        Return a variable of function bound to the node.

        Parameters
        ----------
            variable : str
                The label name of the variable of the bound function.

        Returns
        -------
            FunctionVariable
                The relavant instance of the FunctionVariable class.
        """
        return self.linked_func.func_vars[variable]
    

    def link_function(self, linked_func):
        """
        Bind a function, defined in the implementation, to this node instance.

            Parameters
            ----------
                linked_func : NodeFunction
                    Container class for the variables and function to call for the node instance.
        """
        if not type(linked_func) == "<class 'NodeFunction'>":
            TypeError("Positional argument 'link_func' of 'Node.link_function must be of type NodeFunction.")
            
        self.linked_func = copy.deepcopy(linked_func) #To allow function objects to be re-useable without being modified

        for var in self.linked_func.func_vars.values(): #Tell each variable that it has been bound, this will conrol where it pulls/pushes data when the graph is run
            var.ofNode = self
            

    def __str__(self):
        """
        Called when Node object is printed.

            Returns
            -------
                base_string : str
                    F-string representation of Node instance.
        """
        base_string =  f"""
===== Rattler 'Node' object =====
Title: {self.title}
Id: {self.id}
"""
        return base_string + self.linked_func.__str__()
