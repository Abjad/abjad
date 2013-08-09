# -*- encoding: utf-8 -*-


def is_pitch_carrier(expr):
    '''True when `expr` is an Abjad pitch, note, note-head of chord instance.
    Otherwise false:

    ::

        >>> note = Note("c'4")
        >>> pitchtools.is_pitch_carrier(note)
        True

    Return boolean.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    return isinstance(
        expr, (
            pitchtools.NamedChromaticPitch,
            notetools.Note,
            notetools.NoteHead,
            chordtools.Chord
            )
        )
