from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ObjectSet import ObjectSet


class PitchClassObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Pitch-class set base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###
    
    @abstractmethod
    def __new__(self):
        pass
