def named_chromatic_pitch_tokens_to_named_chromatic_pitches(pitch_tokens):
    '''.. versionadded:: 2.0

    Change named chromatic `pitch_tokens` to named chromatic pitches::

        >>> pitchtools.named_chromatic_pitch_tokens_to_named_chromatic_pitches([0, 2, ('ef', 4)])
        [NamedChromaticPitch("c'"), NamedChromaticPitch("d'"), NamedChromaticPitch("ef'")]

    Return list of zero or more named chromatic pitches.
    '''
    from abjad.tools import pitchtools

    return [pitchtools.NamedChromaticPitch(pitch_token) for pitch_token in pitch_tokens]
