# -*- encoding: utf-8 -*-
import abc

from abjad.tools.pitchtools.NumberedObject import NumberedObject
from abjad.tools.pitchtools.Pitch import Pitch


class NumberedPitch(Pitch, NumberedObject):
    '''Numbered pitch base class from which concrete classes inherit.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
