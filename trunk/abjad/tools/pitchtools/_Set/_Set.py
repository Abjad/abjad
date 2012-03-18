from abc import ABCMeta
from abjad.tools.abctools import ImmutableAbjadObject


class _Set(frozenset, ImmutableAbjadObject):
    '''.. versionadded:: 2.0

    Music-theoretic set base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
