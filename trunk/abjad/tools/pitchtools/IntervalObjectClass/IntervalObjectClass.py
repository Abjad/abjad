import abc
from abjad.tools.abctools import AbjadObject


class IntervalObjectClass(AbjadObject):
    '''.. versionadded:: 2.0

    Interval-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()
    
    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

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
