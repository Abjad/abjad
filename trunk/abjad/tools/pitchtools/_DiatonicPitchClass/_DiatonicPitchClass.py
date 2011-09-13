from abjad.tools.pitchtools._Diatonic import _Diatonic
from abjad.tools.pitchtools._PitchClass import _PitchClass


class _DiatonicPitchClass(_PitchClass, _Diatonic):
    '''.. versionadded:: 2.0

    Diatonic pitch-class base class.
    '''

    ### OVERLOADS ###

    def __abs__(self):
        return self._number

    def __float__(self):
        return float(self._number)

    def __int__(self):
        return self._number

    ### PRIVATE ATTRIBUTES ###

    _diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
        0: 'c', 1: 'd', 2: 'e', 3: 'f', 4: 'g', 5: 'a', 6: 'b'}

    _diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
        'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6}
