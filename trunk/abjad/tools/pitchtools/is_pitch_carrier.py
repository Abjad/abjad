def is_pitch_carrier(expr):
    '''.. versionadded:: 1.1

    True when `expr` is an Abjad pitch, note, note-head of chord instance.
    Otherwise false::

        >>> note = Note("c'4")
        >>> pitchtools.is_pitch_carrier(note)
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``pitchtools.is_carrier()`` to
        ``pitchtools.is_pitch_carrier()``.
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
