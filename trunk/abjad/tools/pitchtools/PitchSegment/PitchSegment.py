# -*- encoding: utf-8 -*-
import abc

from abjad.tools.pitchtools.Segment import Segment


class PitchSegment(Segment):
    '''Pitch segment base class.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
