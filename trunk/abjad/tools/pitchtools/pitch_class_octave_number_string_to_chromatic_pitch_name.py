from abjad.tools.pitchtools.is_pitch_class_octave_number_string import is_pitch_class_octave_number_string
from abjad.tools.pitchtools.is_pitch_class_octave_number_string import pitch_class_octave_number_regex
from abjad.tools.pitchtools.symbolic_accidental_string_to_alphabetic_accidental_abbreviation import symbolic_accidental_string_to_alphabetic_accidental_abbreviation
from abjad.tools.pitchtools.octave_number_to_octave_tick_string import octave_number_to_octave_tick_string


# TODO: implement chromatic_pitch_name_to_pitch_class_octave_number_string()
def pitch_class_octave_number_string_to_chromatic_pitch_name(pitch_class_octave_number_string):
    '''.. versionadded:: 2.5

    Change `pitch_class_octave_number_string` to chromatic pitch name::

        abjad> pitchtools.pitch_class_octave_number_string_to_chromatic_pitch_name('C#+2')
        'ctqs,'

    Return string.
    '''
    
    if not is_pitch_class_octave_number_string(pitch_class_octave_number_string):
        raise ValueError(
            'not pitch-class / octave number string: {!r}.'.format(pitch_class_octave_number_string))
    
    groups = pitch_class_octave_number_regex.match(pitch_class_octave_number_string).groups()
    diatonic_pitch_class_name = groups[0].lower()
    symbolic_accidental_string = groups[1]
    octave_number = int(groups[2])
    alphabetic_accidental_abbreviation = symbolic_accidental_string_to_alphabetic_accidental_abbreviation(
        symbolic_accidental_string)
    octave_tick_string = octave_number_to_octave_tick_string(octave_number)
    chromatic_pitch_class_name = diatonic_pitch_class_name + alphabetic_accidental_abbreviation 
    chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string 

    return chromatic_pitch_name
