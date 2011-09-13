from abjad.tools.pitchtools.chromatic_pitch_name_to_chromatic_pitch_class_name import chromatic_pitch_name_to_chromatic_pitch_class_name
from abjad.tools.pitchtools.diatonic_pitch_name_to_chromatic_pitch_name import diatonic_pitch_name_to_chromatic_pitch_name


def diatonic_pitch_name_to_chromatic_pitch_class_name(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to chromatic pitch-class name::

        abjad> pitchtools.diatonic_pitch_name_to_chromatic_pitch_class_name("c''")
        'c'

    Return string.
    '''

    chromatic_pitch_name = diatonic_pitch_name_to_chromatic_pitch_name(diatonic_pitch_name)

    return chromatic_pitch_name_to_chromatic_pitch_class_name(chromatic_pitch_name)
