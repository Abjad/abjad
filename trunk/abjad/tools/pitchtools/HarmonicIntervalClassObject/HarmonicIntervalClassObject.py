import abc
from abjad.tools.pitchtools.HarmonicObject import HarmonicObject
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class HarmonicIntervalClassObject(IntervalClass, HarmonicObject):
    '''.. versionadded:: 2.0

    Harmonic interval-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
