import abc

from abjad.tools.pitchtools.Set import Set


class PitchSet(Set):
    '''.. versionadded:: 2.0

    Pitch set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
