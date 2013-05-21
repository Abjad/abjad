import abc

from abjad.tools.pitchtools.Segment import Segment


class PitchClassSegment(Segment):
    '''.. versionadded:: 2.0

    Pitch-class segment base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
