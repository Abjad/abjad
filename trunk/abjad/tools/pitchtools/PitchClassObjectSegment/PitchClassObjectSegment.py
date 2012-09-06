import abc

from abjad.tools.pitchtools.ObjectSegment import ObjectSegment


class PitchClassObjectSegment(ObjectSegment):
    '''.. versionadded:: 2.0

    Pitch-class segment base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass
