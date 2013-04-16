import abc
from abjad.tools.pitchtools.Set import Set


class IntervalObjectSet(Set):
    '''.. versionadded:: 2.0

    Abstract interval set.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
