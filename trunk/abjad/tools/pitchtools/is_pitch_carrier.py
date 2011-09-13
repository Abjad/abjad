from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch


def is_pitch_carrier(expr):
    '''.. versionadded:: 1.1

    True when `expr` is an Abjad pitch, note, note-head of chord instance.
    Otherwise false::

        abjad> note = Note("c'4")
        abjad> pitchtools.is_pitch_carrier(note)
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.is_carrier()`` to
        ``pitchtools.is_pitch_carrier()``.
    '''
    from abjad.tools.chordtools.Chord import Chord
    from abjad.tools.notetools.Note import Note
    from abjad.tools.notetools.NoteHead import NoteHead

    return isinstance(expr, (NamedChromaticPitch, Note, NoteHead, Chord))
