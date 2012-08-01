from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import durationtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Command(AbjadObject):
    '''.. versionadded:: 1.0

    Abstract command class from which concrete command classes inherit.

    Basically a fancy tuple.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INTIAILIZER ###

    @abstractmethod
    def __init__(self, value, duration, start_offset, stop_offset):
        duration = durationtools.Duration(duration)
        start_offset = durationtools.Offset(start_offset)
        stop_offset = durationtools.Offset(stop_offset)
        self._value = value
        self._duration = duration
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            for my_value, expr_value in zip(self._mandatory_argument_values, expr._mandatory_argument_values):
                if not my_value == expr_value:
                    return False
            else:
                return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def stop_offset(self):
        return self._stop_offset

    @property
    def value(self):
        return self._value

    @property
    def vector(self):
        return self._mandatory_argument_values
