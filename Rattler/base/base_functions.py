from random import randrange #For generating object id numbers

from . import CustomErrors


class FunctionVariable:
    """
    Contains information on each variable, enabling interpretation of its interaction with a node function. Acts as a port on the node.

    Attributes
    ----------
        label : str
            The label for human interpretation.
        data_type : <type>
            The data type of the variable.
        value : <type>
            The actual value of the variable in an arbitary type.
        id : int
            A random id number to avoid name confusion.
        ofNode : Node
            The node instance that the variable belongs to. Changes pre-decessors/ancestors data will transmit from/to.
    """
    def __init__(self, label, data_type, value=None):
        """
        Constructs attributes for each function variable.

        Parameters
        ----------
        label : str
            The label for human interpretation.
        data_type : <type>
            The data type of the variable.
        value : <type>, optional
            The actual value of the variable in an arbitary type. Default as None.
        """
        self.label = label
        self.data_type = data_type
        self.value = value

        self.ofNode = None
        self.id = randrange(1, 9999999999)

    def __str__(self):
        """
        Called when FunctionVariable object is printed.

            Returns
            -------
                str
                    F-string representation of FunctionVariable instance.
        """
        return f"""

== Variable {self.label} ==
Var Type: {type(self)}
Data Type: {self.data_type}
Value: {self.value}
Id: {self.id}
===========================
"""


class Sink(FunctionVariable):
    """
    Sub-type of FunctionVariable for input variables.

    Methods
    -------
        update(edges_to_exec)
            Updates this sink from the edges ending in it.
    """
    def update(self, edges_to_exec):
        """
        Updates the value of the sink by tracing each edge back to its origin.

        Parameters
        ----------
            edges_to_exec : [int]
                List of edges that terminate at the node this sink belongs to.
        """
        for edge in edges_to_exec:
            if edge.toPort is self:
                self.value = edge.fromPort.value

class Source(FunctionVariable):
    """
    Sub-type of FunctionVariable for output variables.

    Methods
    -------
        update(ret)
            Updates this source to the value provied.
    """
    def update(self, ret):
        """
        Updates this source to the value provided.

        Paramters
        ---------
            ret : <type>
                One of the outputs from the bound function, as approriate to this source.
        """
        self.value = ret



class NodeFunction:
    """
    Associates FunctionVariable objects and the actual function to call for this node to each other.

    Attributes
    ----------
        call : function
            A function that defines the actual operation performed by the node.
        func_vars : {str : FunctionVariable}
            Dict of FunctionVariable instances associated with the operation performed by the node. Keyword is the variable label.

    Methods
    -------
        run(edges_to_exec)
            Execute the function assigned for the variables assocated within the class.
    """
    def __init__(self, call, *func_vars):
        """
        Constructs attributes for the function.

        Parameters
        ----------
            call : function
                A function that defines the actual operation performed by the node, as defined in the implementation.
            *func_vars : FunctionVariable, FunctionVariable, ..
                List of FunctionVariable instances associated with the operation performed by the node.
        """
        self.call = call
        self.func_vars = {var.label:var for var in func_vars}

    def run(self, edges_to_exec = []):
        """
        Updates input variables, executes function, updates output variables.

        Parameters
        ----------
            edges_to_exec : [int], optional
                A list of edges that terminate at the node being run.
        """

        #For each sink update the value from the prior(or none) executed nodes
        #and join it all into a dictionary
        arg_dict = {}
        for var in self.func_vars.values():
            if type(var) is Sink:
                var.update(edges_to_exec)
                arg_dict[var.label] = var.value
             
        ret = [self.call(**arg_dict)] #Call the bound function with a keyword dictionary as the argument
                                      #Run-time determined (by the bound function) length of list is returned

        #Itterate over each source and returned value from the bound function to update source values from returned values
        sources = [var for var in self.func_vars.values() if type(var) is Source]
        for s, r in zip(sources, ret):
            s.update(r)
                
    def __str__(self):
        """
        Called when NodeFunction object is printed.

            Returns
            -------
                base_string : str
                    F-string representation of NodeFunction instance.
        """
        base_string = f"""
Function: {self.call}
"""
        for var in self.func_vars.values(): 
            base_string += var.__str__()
        return base_string
        
        
