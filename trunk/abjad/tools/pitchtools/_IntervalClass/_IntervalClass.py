from abc import ABCMeta
from abjad.tools.abctools import AbjadObject


class _IntervalClass(AbjadObject):
    '''.. versionadded:: 2.0

    Interval-class base class.
    '''

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        return self._number

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return str(self.number)

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        return self._number
