def chromatic_pitch_names_string_to_named_chromatic_pitch_list(chromatic_pitch_names_string):
    '''.. versionadded:: 2.0

    Change `chromatic_pitch_names_string` to named chromatic pitch list::

        >>> string = "cs, cs cs' cs''"
        >>> result = pitchtools.chromatic_pitch_names_string_to_named_chromatic_pitch_list(string)
       
    ::

        >>> for named_chromatic_pitch in result:
        ...     named_chromatic_pitch
        ...
        NamedChromaticPitch('cs,')
        NamedChromaticPitch('cs') 
        NamedChromaticPitch("cs'") 
        NamedChromaticPitch("cs''")

    Return list of named chromatic pitches.
    '''
    from abjad.tools import pitchtools

    pitches = []
    pitch_strings = chromatic_pitch_names_string.split()
    for pitch_string in pitch_strings:
        pitch = pitchtools.NamedChromaticPitch(pitch_string)
        pitches.append(pitch)

    return pitches
