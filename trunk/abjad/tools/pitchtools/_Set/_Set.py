from abc import ABCMeta
from abjad.tools.abctools import AbjadObject


class _Set(frozenset, AbjadObject):
    '''.. versionadded:: 2.0

    Music-theoretic set base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()
