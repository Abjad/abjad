from abjad.tools import sequencetools
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_unordered_named_chromatic_pitch_pairs_in_expr(expr):
    '''.. versionadded:: 2.0

    List unordered named chromatic pitch pairs in `expr`::

        abjad> for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(Chord([0, 1, 2, 3], (1, 4))):
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

    for pair in sequencetools.yield_all_unordered_pairs_of_sequence(sorted(list_named_chromatic_pitches_in_expr(expr))):
        yield pair
