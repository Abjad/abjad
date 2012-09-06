import abc

from abjad.tools.pitchtools.ObjectSet import ObjectSet


class PitchClassObjectSet(ObjectSet):
    '''.. versionadded:: 2.0

    Pitch-class set base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###
    
    @abc.abstractmethod
    def __new__(self):
        pass
