# -*- encoding: utf-8 -*-
import abc

from abjad.tools.pitchtools.Set import Set


class PitchSet(Set):
    '''Pitch set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
