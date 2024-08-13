class CustomErrors:
    class CircularReference(Exception):
        def __init__(self, message="A circular dependency is exists in the node graph."):
            super().__init__(message)

    class EmptyNetwork(Exception):
        def __init__(self, message="An error was raised by performing an operation on an empty graph."):
            super().__init__(message)
