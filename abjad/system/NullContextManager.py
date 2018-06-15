from .ContextManager import ContextManager


class NullContextManager(ContextManager):
    """
    A context manager that does nothing.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __enter__(self):
        """
        Enters context manager and does nothing.
        """
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits context manager and does nothing.
        """
        pass
