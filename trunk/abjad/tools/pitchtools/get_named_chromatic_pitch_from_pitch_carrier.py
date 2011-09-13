from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
import numbers


def get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier):
    '''.. versionadded:: 1.1

    Get named chromatic pitch from `pitch_carrier`::

        abjad> pitch = pitchtools.NamedChromaticPitch('df', 5)
        abjad> pitch
        NamedChromaticPitch("df''")
        abjad> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch)
        NamedChromaticPitch("df''")

    ::

        abjad> note = Note(('df', 5), (1, 4))
        abjad> note
        Note("df''4")
        abjad> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(note)
        NamedChromaticPitch("df''")

    ::

        abjad> note = Note(('df', 5), (1, 4))
        abjad> note.note_head
        NoteHead("df''")
        abjad> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(note.note_head)
        NamedChromaticPitch("df''")

    ::

        abjad> chord = Chord([('df', 5)], (1, 4))
        abjad> chord
        Chord("<df''>4")
        abjad> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(chord)
        NamedChromaticPitch("df''")

    ::

        abjad> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(13)
        NamedChromaticPitch("cs''")

    Raise missing pitch error when `pitch_carrier` carries no pitch.

    Raise extra pitch error when `pitch_carrier` carries more than one pitch.

    Return named chromatic pitch.

    .. versionchanged:: 2.0
        renamed ``pitchtools.get_pitch()`` to
        ``pitchtools.get_named_chromatic_pitch_from_pitch_carrier()``.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools.notetools.NoteHead import NoteHead

    if isinstance(pitch_carrier, NamedChromaticPitch):
        return pitch_carrier
    elif isinstance(pitch_carrier, numbers.Number):
        return NamedChromaticPitch(pitch_carrier)
    elif isinstance(pitch_carrier, Note):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_chromatic_pitch_from_pitch_carrier(pitch)
        else:
            raise MissingPitchError
    elif isinstance(pitch_carrier, NoteHead):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_chromatic_pitch_from_pitch_carrier(pitch)
        else:
            raise MissingPitchError
    elif isinstance(pitch_carrier, Chord):
        pitches = pitch_carrier.written_pitches
        if len(pitches) == 0:
            raise MissingPitchError
        elif len(pitches) == 1:
            return get_named_chromatic_pitch_from_pitch_carrier(pitches[0])
        else:
            raise ExtraPitchError
    else:
        raise TypeError('%s must be Pitch, Note, NoteHead or Chord.' % pitch_carrier)
