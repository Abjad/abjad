from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class PitchObjectSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Pitch segment base class.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(self):
        pass
