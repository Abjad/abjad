# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Set import Set


class IntervalClassSet(Set):
    '''Interval-class set base class.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
