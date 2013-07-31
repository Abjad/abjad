import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextManager(AbjadObject):
    r'''An abstract context manager class.
    '''

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplemented

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplemented

    @abc.abstractmethod
    def __exit__(self):
        raise NotImplemented
