from abc import ABCMeta
from abc import abstractmethod
from experimental.interpretertools.Command import Command


class DivisionToken(Command):
    r'''.. versionadded:: 1.0

    Command indicating durated period of time over which a division-maker will apply.
    
    Bassically a ``(value, duration)`` pair.

    Abstract class from which division tokens inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, value, duration):
        self._value = value
        self._duration = duration

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def vector(self):
        return self._mandatory_argument_values

    @property
    def value(self):
        return self._value
