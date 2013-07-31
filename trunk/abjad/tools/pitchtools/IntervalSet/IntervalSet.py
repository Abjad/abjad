# -*- encoding: utf-8 -*-
import abc
from abjad.tools.pitchtools.Set import Set


class IntervalSet(Set):
    '''.. versionadded:: 2.0

    Abstract interval set.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
