from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.HarmonicObject import HarmonicObject
from abjad.tools.pitchtools.IntervalObject import IntervalObject


class HarmonicIntervalObject(IntervalObject, HarmonicObject):
    '''..versionadded:: 2.0

    Harmonic interval base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
