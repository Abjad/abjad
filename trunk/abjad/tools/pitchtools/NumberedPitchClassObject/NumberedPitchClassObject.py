from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools.NumberedObject import NumberedObject
from abjad.tools.pitchtools.PitchClassObject import PitchClassObject


class NumberedPitchClassObject(PitchClassObject, NumberedObject):
    '''.. versionadded:: 2.0

    Numbered pitch-class base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass
