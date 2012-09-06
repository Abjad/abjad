import abc
from abjad.tools.pitchtools.ChromaticObject import ChromaticObject
from abjad.tools.pitchtools.PitchObject import PitchObject


class ChromaticPitchObject(PitchObject, ChromaticObject):
    '''.. versionadded:: 2.0

    Chromatic pitch base class.
    '''

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass
