from abc import ABCMeta
from abjad.tools.abctools import AttributeEqualityAbjadObject


class _PitchClass(AttributeEqualityAbjadObject):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))
