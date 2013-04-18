import abc
from abjad.tools.pitchtools.Set import Set


class IntervalClassSet(Set):
    '''.. versionadded:: 2.0

    Interval-class set base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
