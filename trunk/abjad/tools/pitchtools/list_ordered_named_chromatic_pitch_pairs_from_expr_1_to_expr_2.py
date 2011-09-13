from abjad.tools import sequencetools
from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr


def list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(expr_1, expr_2):
    '''.. versionadded:: 2.0

    List ordered named chromatic pitch pairs from `expr_1` to `expr_2`::

        abjad> chord_1 = Chord([0, 1, 2], (1, 4))
        abjad> chord_2 = Chord([3, 4], (1, 4))
        abjad> for pair in pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(chord_1, chord_2):
        ...        pair
        (NamedChromaticPitch("c'"), NamedChromaticPitch("ef'"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("e'"))
        (NamedChromaticPitch("cs'"), NamedChromaticPitch("ef'"))
        (NamedChromaticPitch("cs'"), NamedChromaticPitch("e'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("ef'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("e'"))

    Return generator.
    '''

    pitches_1 = sorted(list_named_chromatic_pitches_in_expr(expr_1))
    pitches_2 = sorted(list_named_chromatic_pitches_in_expr(expr_2))
    for pair in sequencetools.yield_all_pairs_between_sequences(pitches_1, pitches_2):
        yield pair
