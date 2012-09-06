import abc

from abjad.tools.abctools import AttributeEqualityAbjadObject


class PitchClassObject(AttributeEqualityAbjadObject):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INNITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))
