from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.abctools.AbjadObject import AbjadObject


class Command(AbjadObject):
    '''.. versionadded:: 1.0

    Abstract command class from which concrete command classes inherit.

    Basically a ``(value, duration)`` pair.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INTIAILIZER ###

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
