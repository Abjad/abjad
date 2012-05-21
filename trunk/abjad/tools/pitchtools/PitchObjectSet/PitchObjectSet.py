from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class PitchObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Pitch set base class.
    '''

    ### CLASS METHODS ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(self):
        pass
