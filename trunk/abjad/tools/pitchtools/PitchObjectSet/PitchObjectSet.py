import abc

from abjad.tools.pitchtools.ObjectSet import ObjectSet


class PitchObjectSet(ObjectSet):
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
