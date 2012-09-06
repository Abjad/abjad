import abc

from abjad.tools.pitchtools.DiatonicObject import DiatonicObject
from abjad.tools.pitchtools.PitchClassObject import PitchClassObject


class DiatonicPitchClassObject(PitchClassObject, DiatonicObject):
    '''.. versionadded:: 2.0

    Diatonic pitch-class base class.
    '''

    ### CLASSS ATTRIBUTES ###

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

    ### PRIVATE PROPERTIES ###

    _diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
        0: 'c', 1: 'd', 2: 'e', 3: 'f', 4: 'g', 5: 'a', 6: 'b'}

    _diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
        'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6}
