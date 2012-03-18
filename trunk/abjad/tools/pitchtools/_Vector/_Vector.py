from abc import ABCMeta
from abjad.tools.datastructuretools import ImmutableDictionary


class _Vector(ImmutableDictionary):
    '''.. versionadded:: 2.0

    (Music theoretic) vector base class.
    '''

    __metaclass__ = ABCMeta
