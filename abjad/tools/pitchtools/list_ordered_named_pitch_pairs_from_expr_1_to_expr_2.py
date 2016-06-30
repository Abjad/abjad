# -*- coding: utf-8 -*-
from abjad.tools import sequencetools


def list_ordered_named_pitch_pairs_from_expr_1_to_expr_2(expr_1, expr_2):
    '''Lists ordered named pitch pairs from `expr_1` to `expr_2`.

    ::

        >>> chord_1 = Chord([0, 1, 2], (1, 4))
        >>> chord_2 = Chord([3, 4], (1, 4))

    ::

        >>> for pair in pitchtools.list_ordered_named_pitch_pairs_from_expr_1_to_expr_2(
        ...     chord_1, chord_2):
        ...     pair
        (NamedPitch("c'"), NamedPitch("ef'"))
        (NamedPitch("c'"), NamedPitch("e'"))
        (NamedPitch("cs'"), NamedPitch("ef'"))
        (NamedPitch("cs'"), NamedPitch("e'"))
        (NamedPitch("d'"), NamedPitch("ef'"))
        (NamedPitch("d'"), NamedPitch("e'"))

    Returns generator.
    '''
    from abjad.tools import pitchtools

    pitches_1 = sorted(pitchtools.list_named_pitches_in_expr(expr_1))
    pitches_2 = sorted(pitchtools.list_named_pitches_in_expr(expr_2))
    for pair in sequencetools.yield_all_pairs_between_sequences(pitches_1, pitches_2):
        yield pair