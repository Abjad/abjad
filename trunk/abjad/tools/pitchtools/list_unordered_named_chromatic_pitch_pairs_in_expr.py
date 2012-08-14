from abjad.tools import sequencetools


def list_unordered_named_chromatic_pitch_pairs_in_expr(expr):
    '''.. versionadded:: 2.0

    List unordered named chromatic pitch pairs in `expr`::

        >>> chord = Chord("<c' cs' d' ef'>4")

    ::

        >>> for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(chord):
        ...     pair
        ...
        (NamedChromaticPitch("c'"), NamedChromaticPitch("cs'"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("d'"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("ef'"))
        (NamedChromaticPitch("cs'"), NamedChromaticPitch("d'"))
        (NamedChromaticPitch("cs'"), NamedChromaticPitch("ef'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("ef'"))

    Return generator.
    '''
    from abjad.tools import pitchtools

    for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
        sorted(pitchtools.list_named_chromatic_pitches_in_expr(expr))):
        yield pair
