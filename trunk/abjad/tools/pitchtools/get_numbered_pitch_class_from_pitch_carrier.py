# -*- encoding: utf-8 -*-


def get_numbered_pitch_class_from_pitch_carrier(pitch_carrier):
    '''Get numbered chromatic pitch-class from `pitch_carrier`:

    ::

        >>> note = Note("cs'4")
        >>> pitchtools.get_numbered_pitch_class_from_pitch_carrier(note)
        NumberedPitchClass(1)

    Raise missing pitch error on empty chords.

    Raise extra pitch error on many-note chords.

    Return numbered chromatic pitch-class.
    '''
    from abjad.tools import pitchtools

    pitch = pitchtools.get_named_pitch_from_pitch_carrier(pitch_carrier)
    pitch_class = pitchtools.NumberedPitchClass(pitch)

    return pitch_class
