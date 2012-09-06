import abc
from abjad.tools.pitchtools.HarmonicObject import HarmonicObject
from abjad.tools.pitchtools.IntervalObject import IntervalObject


class HarmonicIntervalObject(IntervalObject, HarmonicObject):
    '''..versionadded:: 2.0

    Harmonic interval base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
