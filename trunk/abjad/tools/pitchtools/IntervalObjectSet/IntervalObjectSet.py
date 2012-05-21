from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class IntervalObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Abstract interval set.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __new__(self):
        pass
