from abjad.tools.chordtools.Chord import Chord
from abjad.decorators import requires
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools import pitchtools
from numbers import Number


@requires(Chord, pitchtools.is_named_chromatic_pitch_token)
def get_note_head_from_chord_by_pitch(chord, pitch):
    '''.. versionadded:: 2.0

    Get note head from `chord` by `pitch`::

        abjad> chord = Chord("<c'' d'' b''>4")

    ::

        abjad> chordtools.get_note_head_from_chord_by_pitch(chord, 14)
        NoteHead("d''")

    Raise missing note head error when `chord` contains no 
    note head with pitch equal to `pitch`.

    Raise extra note head error when `chord` contains more than 
    one note head with pitch equal to `pitch`.

    .. versionchanged:: 2.0
        renamed ``chordtools.get_note_head()`` to
        ``chordtools.get_note_head_from_chord_by_pitch()``.
    '''

    result = []

    if isinstance(pitch, NamedChromaticPitch):
        for note_head in chord.note_heads:
            if note_head.written_pitch == pitch:
                result.append(note_head)
    else:
        for note_head in chord.note_heads:
            if note_head.written_pitch.numbered_chromatic_pitch._chromatic_pitch_number == pitch:
                result.append(note_head)

    count = len(result)

    if count == 0:
        raise MissingNoteHeadError
    elif count == 1:
        note_head = result[0]
        return note_head
    else:
        raise ExtraNoteHeadError
