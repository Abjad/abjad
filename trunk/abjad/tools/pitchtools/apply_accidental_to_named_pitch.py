# -*- encoding: utf-8 -*-


def apply_accidental_to_named_pitch(named_pitch, accidental=None):
    '''Apply `accidental` to `named_pitch`:

    ::

        >>> pitch = pitchtools.NamedPitch("cs''")
        >>> pitchtools.apply_accidental_to_named_pitch(pitch, 'f')
        NamedPitch("c''")

    Return new named pitch.
    '''
    return named_pitch.apply_accidental(accidental)
