from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.NumberedObject import NumberedObject
from abjad.tools.pitchtools.PitchObject import PitchObject


class NumberedPitchObject(PitchObject, NumberedObject):
    '''.. versionadded:: 2.0

    Numbered pitch base class from which concrete classes inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
