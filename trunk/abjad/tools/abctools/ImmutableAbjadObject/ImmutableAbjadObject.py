from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class ImmutableAbjadObject(AbjadObject):
    '''.. versionadded:: 2.8

    Abstract base class from which all custom classes which also subclass
    immutable builtin classes, such as tuple and frozenset, should inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(klass, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        pass
