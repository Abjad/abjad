import abc
from abjad.tools.pitchtools.HarmonicObject import HarmonicObject
from abjad.tools.pitchtools.Interval import Interval


class HarmonicInterval(Interval, HarmonicObject):
    '''..versionadded:: 2.0

    Harmonic interval base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
