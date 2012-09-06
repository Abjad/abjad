import abc

from abjad.tools.pitchtools.DiatonicObject import DiatonicObject
from abjad.tools.pitchtools.PitchObject import PitchObject


class DiatonicPitchObject(PitchObject, DiatonicObject):
    '''.. versionadded:: 2.0

    Diatonic pitch base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ()


    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        return self._number

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number
