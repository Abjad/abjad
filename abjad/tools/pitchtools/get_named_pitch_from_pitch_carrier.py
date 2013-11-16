# -*- encoding: utf-8 -*-
import numbers


def get_named_pitch_from_pitch_carrier(pitch_carrier):
    '''Gets named pitch from `pitch_carrier`.

    ::

        >>> pitch = NamedPitch('df', 5)
        >>> pitch
        NamedPitch("df''")
        >>> pitchtools.get_named_pitch_from_pitch_carrier(pitch)
        NamedPitch("df''")

    ::

        >>> note = Note(('df', 5), (1, 4))
        >>> note
        Note("df''4")
        >>> pitchtools.get_named_pitch_from_pitch_carrier(note)
        NamedPitch("df''")

    ::

        >>> note = Note(('df', 5), (1, 4))
        >>> note.note_head
        NoteHead("df''")
        >>> pitchtools.get_named_pitch_from_pitch_carrier(note.note_head)
        NamedPitch("df''")

    ::

        >>> chord = Chord([('df', 5)], (1, 4))
        >>> chord
        Chord("<df''>4")
        >>> pitchtools.get_named_pitch_from_pitch_carrier(chord)
        NamedPitch("df''")

    ::

        >>> pitchtools.get_named_pitch_from_pitch_carrier(13)
        NamedPitch("cs''")

    Raise value error when `pitch_carrier` carries no pitch.

    Raises value error when `pitch_carrier` carries more than one pitch.

    Returns named pitch.
    '''
    from abjad.tools import scoretools
    from abjad.tools import scoretools
    from abjad.tools import pitchtools

    if isinstance(pitch_carrier, pitchtools.NamedPitch):
        return pitch_carrier
    elif isinstance(pitch_carrier, pitchtools.NumberedPitch):
        return pitchtools.NamedPitch(pitch_carrier)
    elif isinstance(pitch_carrier, numbers.Number):
        return pitchtools.NamedPitch(pitch_carrier)
    elif isinstance(pitch_carrier, scoretools.Note):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_pitch_from_pitch_carrier(pitch)
        else:
            message = 'no pitch found on {!r}.'
            message = message.format(pitch_carrier)
            raise ValueError(message)
    elif isinstance(pitch_carrier, scoretools.NoteHead):
        pitch = pitch_carrier.written_pitch
        if pitch is not None:
            return get_named_pitch_from_pitch_carrier(pitch)
        else:
            message = 'no pitch found on {!r}.'
            message = message.format(pitch_carrier)
            raise ValueError(message)
    elif isinstance(pitch_carrier, scoretools.Chord):
        pitches = pitch_carrier.written_pitches
        if len(pitches) == 0:
            message = 'no pitch found on {!r}.'
            message = message.format(pitch_carrier)
            raise ValueError(message)
        elif len(pitches) == 1:
            return get_named_pitch_from_pitch_carrier(pitches[0])
        else:
            message = 'multiple pitches found on {!r}.'
            message = message.format(pitch_carrier)
            raise ValueError(message)
    else:
        message = 'pitch carrier {!r} must be pitch, note, note head or chord.'
        message = message.format(pitch_carrier)
        raise TypeError(message)
