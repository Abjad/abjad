def analyze_tonal_function(expr, key_signature):
    '''.. versionadded:: 2.0

    Analyze `expr` and return tonal function according to `key_signature`. ::

        >>> from abjad.tools import tonalitytools

    ::

        >>> chord = Chord(['ef', 'g', 'bf'], (1, 4))
        >>> key_signature = contexttools.KeySignatureMark('c', 'major')
        >>> tonalitytools.analyze_tonal_function(chord, key_signature)
        FlatIIIMajorTriadInRootPosition

    Return none when no tonal function is understood. ::

        >>> chord = Chord(['c', 'cs', 'd'], (1, 4))
        >>> key_signature = contexttools.KeySignatureMark('c', 'major')
        >>> tonalitytools.analyze_tonal_function(chord, key_signature) is None
        True

    Return tonal function or none.
    '''
    from abjad.tools import tonalitytools

    if isinstance(expr, tonalitytools.ChordClass):
        chord_class = expr
    else:
        chord_class = tonalitytools.analyze_chord(expr)

    if chord_class is None:
        return None

    root = chord_class.root
    scale = tonalitytools.Scale(key_signature)
    scale_degree = scale.named_chromatic_pitch_class_to_scale_degree(root)
    quality = chord_class.quality_indicator.quality_string
    extent = chord_class.extent
    inversion = chord_class.inversion

    tonal_function = tonalitytools.TonalFunction(scale_degree, quality, extent, inversion)
    return tonal_function
