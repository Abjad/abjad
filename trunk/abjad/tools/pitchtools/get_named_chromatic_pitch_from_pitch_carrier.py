import numbers


def get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier):
    '''.. versionadded:: 1.1

    Get named chromatic pitch from `pitch_carrier`::

        >>> pitch = pitchtools.NamedChromaticPitch('df', 5)
        >>> pitch
        NamedChromaticPitch("df''")
        >>> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(pitch)
        NamedChromaticPitch("df''")

    ::

        >>> note = Note(('df', 5), (1, 4))
        >>> note
        Note("df''4")
        >>> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(note)
        NamedChromaticPitch("df''")

    ::

        >>> note = Note(('df', 5), (1, 4))
        >>> note.note_head
        NoteHead("df''")
        >>> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(note.note_head)
        NamedChromaticPitch("df''")

    ::

        >>> chord = Chord([('df', 5)], (1, 4))
        >>> chord
        Chord("<df''>4")
        >>> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(chord)
        NamedChromaticPitch("df''")

    ::

        >>> pitchtools.get_named_chromatic_pitch_from_pitch_carrier(13)
        NamedChromaticPitch("cs''")

    Raise missing pitch error when `pitch_carrier` carries no pitch.

    Raise extra pitch error when `pitch_carrier` carries more than one pitch.

    Return named chromatic pitch.

    .. versionchanged:: 2.0
        renamed ``pitchtools.get_pitch()`` to
        ``pitchtools.get_named_chromatic_pitch_from_pitch_carrier()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import pitchtools

    if isinstance(pitch_carrier, pitchtools.NamedChromaticPitch):
        return pitch_carrier
    elif isinstance(pitch_carrier, numbers.Number):
        return pitchtools.NamedChromaticPitch(pitch_carrier)
    elif isinstance(pitch_carrier, notetools.Note):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_chromatic_pitch_from_pitch_carrier(pitch)
        else:
            raise MissingPitchError
    elif isinstance(pitch_carrier, notetools.NoteHead):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_chromatic_pitch_from_pitch_carrier(pitch)
        else:
            raise MissingPitchError
    elif isinstance(pitch_carrier, chordtools.Chord):
        pitches = pitch_carrier.written_pitches
        if len(pitches) == 0:
            raise MissingPitchError
        elif len(pitches) == 1:
            return get_named_chromatic_pitch_from_pitch_carrier(pitches[0])
        else:
            raise ExtraPitchError
    else:
        raise TypeError('%s must be Pitch, Note, NoteHead or Chord.' % pitch_carrier)
