from abjad.tools.notetools.Note import Note
from abjad.tools.resttools.Rest import Rest
from abjad.exceptions import InputSpecificationError
from abjad.tools import pitchtools
from abjad.tools.lilypondfiletools._lilypond_leaf_regex import _lilypond_leaf_regex
from abjad.tools.lilypondfiletools._parse_chord_entry_token import _parse_chord_entry_token
from abjad.tools.resttools.MultiMeasureRest import MultiMeasureRest
from abjad.tools.skiptools.Skip import Skip
import re


def _parse_note_entry_token(note_entry_token):
    '''.. versionadded:: 2.0

    Parse simple LilyPond `note_entry_token`.

    Return leaf.
    '''

    if not isinstance(note_entry_token, str):
        raise TypeError('LilyPond input token must be string.')

    pattern = _lilypond_leaf_regex
    match = re.match(pattern, note_entry_token)
    if match is None:
        # TODO: make this work; change outer loop. #
        #if note_entry_token.startswith('<'):
        #   chord = _parse_chord_entry_token(note_entry_token)
        #   return chord
        message = 'incorrect note entry token: %s.\n' % note_entry_token
        raise InputSpecificationError(message)

    name, ticks, duration_body, dots = match.groups()
    duration_string = duration_body + dots

    if name == 'r':
        return Rest(duration_string)
    elif name == 'R':
        return MultiMeasureRest(duration_string)
    elif name == 's':
        return Skip(duration_string)
    else:
        pitch_string = name + ticks
        pitch = pitchtools.NamedChromaticPitch(pitch_string)
        return Note(pitch, duration_string)
