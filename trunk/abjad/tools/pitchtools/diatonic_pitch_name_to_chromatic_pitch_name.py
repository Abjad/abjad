from abjad.tools.pitchtools.is_diatonic_pitch_name import is_diatonic_pitch_name


def diatonic_pitch_name_to_chromatic_pitch_name(diatonic_pitch_name):
    '''.. versionadded:: 2.0

    Change `diatonic_pitch_name` to chromatic pitch name::

        abjad> pitchtools.diatonic_pitch_name_to_chromatic_pitch_name("c''")
        "c''"

    Return string.
    '''

    if not is_diatonic_pitch_name(diatonic_pitch_name):
        raise TypeError

    return diatonic_pitch_name
