import abc
from abjad.tools.pitchtools.ChromaticObject import ChromaticObject
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class ChromaticIntervalClass(IntervalClass, ChromaticObject):
    '''.. versionadded:: 2.0

    Chromatic interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        return type(self)(abs(self._number))

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
