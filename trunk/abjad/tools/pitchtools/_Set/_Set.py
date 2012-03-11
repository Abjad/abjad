from abc import ABCMeta
from abjad.tools.abctools import Immutable


class _Set(frozenset, Immutable):
    '''.. versionadded:: 2.0

    Music-theoretic set base class.
    '''

    __metaclass__ = ABCMeta

    pass
