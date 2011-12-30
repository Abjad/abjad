from abjad.tools.pitchtools.is_pitch_class_octave_number_string import is_pitch_class_octave_number_string
from abjad.tools.pitchtools.is_pitch_class_octave_number_string import pitch_class_octave_number_regex


def pitch_class_octave_number_string_to_chromatic_pitch_name(pitch_class_octave_number_string):
    '''.. versionadded:: 2.5

    Change `pitch_class_octave_number_string` to chromatic pitch name.

    Return string.
    '''
    
    if not is_pitch_class_octave_number_string(pitch_class_octave_number_string):
        raise ValueError(
        'not pitch-class / octave number string: {!r}'.format(pitch_class_octave_number_string))
    
    groups = pitch_class_octave_number_regex.match(pitch_class_octave_number_string).groups()
    print groups
    
    diatonic_pitch_class_name = groups[0].lower()
    symbolic_accidental_string = groups[1]
    octave_number = int(groups[2])

    print '{!r} {!r} {!r}'.format(diatonic_pitch_class_name, symbolic_accidental_string, octave_number)
