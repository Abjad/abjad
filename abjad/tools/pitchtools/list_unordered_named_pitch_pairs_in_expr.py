# -*- coding: utf-8 -*-
from abjad.tools import sequencetools


def list_unordered_named_pitch_pairs_in_expr(expr):
    '''Lists unordered named pitch pairs in `expr`.

    ::

        >>> chord = Chord("<c' cs' d' ef'>4")

    ::

        >>> for pair in pitchtools.list_unordered_named_pitch_pairs_in_expr(chord):
        ...     pair
        ...
        (NamedPitch("c'"), NamedPitch("cs'"))
        (NamedPitch("c'"), NamedPitch("d'"))
        (NamedPitch("c'"), NamedPitch("ef'"))
        (NamedPitch("cs'"), NamedPitch("d'"))
        (NamedPitch("cs'"), NamedPitch("ef'"))
        (NamedPitch("d'"), NamedPitch("ef'"))

    Returns generator.
    '''
    from abjad.tools import pitchtools

    for pair in sequencetools.yield_all_unordered_pairs_of_sequence(
        sorted(pitchtools.list_named_pitches_in_expr(expr))):
        yield pair