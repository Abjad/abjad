import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextManager(AbjadObject):
    '''An abstract context manager class.'''

    @abc.abstractmethod
    def __init__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __exit__(self):
        raise NotImplemented
