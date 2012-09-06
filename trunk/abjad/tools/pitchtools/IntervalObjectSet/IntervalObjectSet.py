import abc
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class IntervalObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Abstract interval set.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
