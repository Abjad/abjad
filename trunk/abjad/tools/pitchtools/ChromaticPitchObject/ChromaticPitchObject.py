from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.ChromaticObject import ChromaticObject
from abjad.tools.pitchtools.PitchObject import PitchObject


class ChromaticPitchObject(PitchObject, ChromaticObject):
    '''.. versionadded:: 2.0

    Chromatic pitch base class.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
