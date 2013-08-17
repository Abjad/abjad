# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Interval import Interval


class HarmonicInterval(Interval):
    '''Harmonic interval base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
