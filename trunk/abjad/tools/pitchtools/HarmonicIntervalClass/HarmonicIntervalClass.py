# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.IntervalClass import IntervalClass


class HarmonicIntervalClass(IntervalClass):
    '''Harmonic interval-class base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
