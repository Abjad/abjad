import abc
from abjad.system.AbjadObject import AbjadObject


class ContextManager(AbjadObject):
    """
    An abstract context manager class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __enter__(self):
        """
        Enters context manager.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits context manager.
        """
        raise NotImplementedError
