from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools import AttributeEqualityAbjadObject


class PitchClassObject(AttributeEqualityAbjadObject):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INNITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))
