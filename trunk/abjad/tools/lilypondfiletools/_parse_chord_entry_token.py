import re
from abjad.tools import chordtools
from abjad.tools import durationtools


# TODO: remove altogether in favor of LilyPondParser
def _parse_chord_entry_token(chord_entry_token):
    '''.. versionadded:: 2.0

    Parse LilyPond-style `chord_entry_token`.
    '''

    pattern = '^<(.+)>\s*(.+)'
    match = re.match(pattern, chord_entry_token)

    if match is None:
        message = 'incorrect chord entry token %s.' % chord_entry_token
        raise InputSpecificationError(message)

    pitch_string, duration_string = match.groups()
    pitch_list = pitch_string.split()
    duration = durationtools.lilypond_duration_string_to_rational(duration_string)
    chord = chordtools.Chord(pitch_list, duration)

    return chord
