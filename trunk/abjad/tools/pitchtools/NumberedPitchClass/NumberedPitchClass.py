# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.PitchClass import PitchClass


class NumberedPitchClass(PitchClass):
    '''Numbered pitch-class base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
