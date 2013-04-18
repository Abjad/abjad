import abc
from abjad.tools.pitchtools.CounterpointObject import CounterpointObject
from abjad.tools.pitchtools.Interval import Interval


class CounterpointIntervalObject(Interval, CounterpointObject):
    '''..versionadded:: 2.0

    Counterpoint interval base class.
    '''

    ### CLASS ATTRIBUTES ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def number(self):
        return self._number

    @property
    def semitones(self):
        raise NotImplementedError
