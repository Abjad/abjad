import abc

from abjad.tools.pitchtools.Segment import Segment


class PitchSegment(Segment):
    '''.. versionadded:: 2.0

    Pitch segment base class.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
