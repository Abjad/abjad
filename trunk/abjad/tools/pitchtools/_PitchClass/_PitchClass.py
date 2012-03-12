from abc import ABCMeta
from abjad.tools.abctools import AttributeEqualityAbjadObject
from abjad.tools.abctools import ImmutableAbjadObject


class _PitchClass(ImmutableAbjadObject, AttributeEqualityAbjadObject):
    '''.. versionadded:: 2.0

    Pitch-class base class.
    '''

    __metaclass__ = ABCMeta

    ### OVERLOADS ###

    def __hash__(self):
        return hash(repr(self))
