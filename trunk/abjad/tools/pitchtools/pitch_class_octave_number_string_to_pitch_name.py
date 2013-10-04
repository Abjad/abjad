# -*- encoding: utf-8 -*-
# TODO: implement pitch_name_to_pitch_class_octave_number_string()
def pitch_class_octave_number_string_to_pitch_name(pitch_class_octave_number_string):
    '''Change `pitch_class_octave_number_string` to chromatic pitch name:

    ::

        >>> pitchtools.pitch_class_octave_number_string_to_pitch_name('C#+2')
        'ctqs,'

    Return string.
    '''
    from abjad.tools import pitchtools

    if not pitchtools.is_pitch_class_octave_number_string(pitch_class_octave_number_string):
        raise ValueError(
            'not pitch-class / octave number string: {!r}.'.format(pitch_class_octave_number_string))

    groups = pitchtools.Pitch._pitch_class_octave_number_regex.match(
        pitch_class_octave_number_string).groups()
    diatonic_pitch_class_name = groups[0].lower()
    symbolic_accidental_string = groups[1]
    octave_number = int(groups[2])
    alphabetic_accidental_abbreviation = \
        pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation(
        symbolic_accidental_string)
    octave_tick_string = str(pitchtools.OctaveIndication(octave_number))
    pitch_class_name = diatonic_pitch_class_name + alphabetic_accidental_abbreviation
    pitch_name = pitch_class_name + octave_tick_string

    return pitch_name
