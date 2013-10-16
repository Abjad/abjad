# -*- encoding: utf-8 -*-


def transpose_named_pitch_by_numbered_interval_and_respell(
    pitch, staff_spaces, melodic_chromatic_interval):
    '''Transpose named pitch by `melodic_chromatic_interval` and respell `staff_spaces`
    above or below:

    ::

        >>> pitch = pitchtools.NamedPitch(0)

    ::

        >>> pitchtools.transpose_named_pitch_by_numbered_interval_and_respell(
        ...     pitch, 1, 0.5)
        NamedPitch("dtqf'")

    Return new named pitch.
    '''
    from abjad.tools import pitchtools

    pitch_number = pitch.pitch_number + melodic_chromatic_interval
    diatonic_pitch_class_number = (pitch.diatonic_pitch_class_number + staff_spaces) % 7
    diatonic_pitch_class_name = \
        pitchtools.PitchClass._diatonic_pitch_class_number_to_diatonic_pitch_class_name[
            diatonic_pitch_class_number]
    return pitchtools.NamedPitch(pitch_number, diatonic_pitch_class_name)
