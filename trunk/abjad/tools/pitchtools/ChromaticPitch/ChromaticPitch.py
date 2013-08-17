# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Pitch import Pitch


class ChromaticPitch(Pitch):
    '''Chromatic pitch base class.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
