import abc
from abjad.tools.pitchtools.CounterpointObject import CounterpointObject
from abjad.tools.pitchtools.IntervalObjectClass import IntervalObjectClass


class CounterpointIntervalClassObject(IntervalObjectClass, CounterpointObject):
    '''.. versionadded:: 2.0

    Counterpoint interval-class base class.
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

    def __int__(self):
        return self._number
