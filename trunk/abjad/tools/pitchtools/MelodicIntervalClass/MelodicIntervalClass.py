# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class MelodicIntervalClass(IntervalClass):
    '''Melodic interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass


