from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class IntervalClassObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Interval-class set base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __new__(self):
        pass
