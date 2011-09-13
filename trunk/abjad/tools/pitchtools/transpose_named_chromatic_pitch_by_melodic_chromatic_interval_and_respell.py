from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.diatonic_pitch_class_number_to_diatonic_pitch_class_name import diatonic_pitch_class_number_to_diatonic_pitch_class_name

def transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(
    pitch, staff_spaces, melodic_chromatic_interval):
    '''.. versionadded:: 1.1

    Transpose named chromatic pitch by `melodic_chromatic_interval` and respell `staff_spaces`
    above or below::

        abjad> pitch = pitchtools.NamedChromaticPitch(0)
        abjad> pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell(pitch, 1, 0.5)
        NamedChromaticPitch("dtqf'")

    Return new named chromatic pitch.

    .. versionchanged:: 2.0
        renamed ``pitchtools.staff_space_transpose()`` to
        ``pitchtools.transpose_named_chromatic_pitch_by_melodic_chromatic_interval_and_respell()``.
    '''

    chromatic_pitch_number = pitch.chromatic_pitch_number + melodic_chromatic_interval
    diatonic_pitch_class_number = (pitch.diatonic_pitch_class_number + staff_spaces) % 7
    diatonic_pitch_class_name = diatonic_pitch_class_number_to_diatonic_pitch_class_name(
        diatonic_pitch_class_number)
    return NamedChromaticPitch(chromatic_pitch_number, diatonic_pitch_class_name)
