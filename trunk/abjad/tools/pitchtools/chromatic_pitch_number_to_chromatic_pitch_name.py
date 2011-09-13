from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name import chromatic_pitch_class_number_to_chromatic_pitch_class_name
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats
from abjad.tools.pitchtools.chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps import chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps
from abjad.tools.pitchtools.is_chromatic_pitch_number import is_chromatic_pitch_number
from abjad.tools.pitchtools.octave_number_to_octave_tick_string import octave_number_to_octave_tick_string


def chromatic_pitch_number_to_chromatic_pitch_name(
    chromatic_pitch_number, accidental_spelling = 'mixed'):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_number` to chromatic pitch name::

        abjad> pitchtools.chromatic_pitch_number_to_chromatic_pitch_name(13)
        "cs''"

    Return string.
    '''

    if not is_chromatic_pitch_number(chromatic_pitch_number):
        raise ValueError('\n\tNot chromatic pitch number: "%s".' % chromatic_pitch_number)

    if not isinstance(accidental_spelling, str):
        raise TypeError

    if not accidental_spelling in ('mixed', 'flats', 'sharps'):
        raise ValueError

    chromatic_pitch_class_number = chromatic_pitch_number % 12

    if accidental_spelling == 'mixed':
        chromatic_pitch_class_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name(
            chromatic_pitch_class_number)
    elif accidental_spelling == 'sharps':
        chromatic_pitch_class_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_sharps(
            chromatic_pitch_class_number)
    elif accidental_spelling == 'flats':
        chromatic_pitch_class_name = chromatic_pitch_class_number_to_chromatic_pitch_class_name_with_flats(
            chromatic_pitch_class_number)
    else:
        raise ValueError('unknown accidental spelling: "%s".' % accidental_spelling)

    octave_number = chromatic_pitch_number // 12 + 4
    octave_tick_string = octave_number_to_octave_tick_string(octave_number)

    chromatic_pitch_name = chromatic_pitch_class_name + octave_tick_string

    return chromatic_pitch_name
