import abc

from .StorageFormatManager import StorageFormatManager


class ContextManager(object):
    """
    An abstract context manager class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _is_abstract = True

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()
