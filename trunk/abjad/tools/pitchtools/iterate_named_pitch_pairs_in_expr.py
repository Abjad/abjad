# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


def iterate_named_pitch_pairs_in_expr(expr):
    r'''Iterate left-to-right, top-to-bottom named pitch pairs in `expr`:

    ::

        >>> score = Score([])
        >>> notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'4")]
        >>> score.append(Staff(notes))
        >>> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
        >>> score.append(Staff(notes))
        >>> contexttools.ClefMark('bass')(score[1])
        ClefMark('bass')(Staff{3})

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
                g'4
            }
            \new Staff {
                \clef "bass"
                c4
                a,4
                g,4
            }
        >>

    ::

        >>> for pair in pitchtools.iterate_named_pitch_pairs_in_expr(score):
        ...     pair
        ...
        (NamedPitch("c'"), NamedPitch('c'))
        (NamedPitch("c'"), NamedPitch("d'"))
        (NamedPitch('c'), NamedPitch("d'"))
        (NamedPitch("d'"), NamedPitch("e'"))
        (NamedPitch("d'"), NamedPitch('a,'))
        (NamedPitch('c'), NamedPitch("e'"))
        (NamedPitch('c'), NamedPitch('a,'))
        (NamedPitch("e'"), NamedPitch('a,'))
        (NamedPitch("e'"), NamedPitch("f'"))
        (NamedPitch('a,'), NamedPitch("f'"))
        (NamedPitch("f'"), NamedPitch("g'"))
        (NamedPitch("f'"), NamedPitch('g,'))
        (NamedPitch('a,'), NamedPitch("g'"))
        (NamedPitch('a,'), NamedPitch('g,'))
        (NamedPitch("g'"), NamedPitch('g,'))

    Chords are handled correctly. ::

        >>> chord_1 = Chord([0, 2, 4], (1, 4))
        >>> chord_2 = Chord([17, 19], (1, 4))
        >>> staff = Staff([chord_1, chord_2])

    ..  doctest::

        >>> f(staff)
        \new Staff {
            <c' d' e'>4
            <f'' g''>4
        }

    ::

        >>> for pair in pitchtools.iterate_named_pitch_pairs_in_expr(staff):
        ...   print pair
        (NamedPitch("c'"), NamedPitch("d'"))
        (NamedPitch("c'"), NamedPitch("e'"))
        (NamedPitch("d'"), NamedPitch("e'"))
        (NamedPitch("c'"), NamedPitch("f''"))
        (NamedPitch("c'"), NamedPitch("g''"))
        (NamedPitch("d'"), NamedPitch("f''"))
        (NamedPitch("d'"), NamedPitch("g''"))
        (NamedPitch("e'"), NamedPitch("f''"))
        (NamedPitch("e'"), NamedPitch("g''"))
        (NamedPitch("f''"), NamedPitch("g''"))

    Returns generator.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import pitchtools

    for leaf_pair in iterationtools.iterate_leaf_pairs_in_expr(expr):
        leaf_pair_list = list(leaf_pair)
        # iterate chord pitches if first leaf is chord
        for pair in pitchtools.list_unordered_named_pitch_pairs_in_expr(leaf_pair_list[0]):
            yield pair
        if isinstance(leaf_pair, set):
            for pair in pitchtools.list_unordered_named_pitch_pairs_in_expr(leaf_pair):
                yield pair
        elif isinstance(leaf_pair, tuple):
            for pair in pitchtools.list_ordered_named_pitch_pairs_from_expr_1_to_expr_2(*leaf_pair):
                yield pair
        else:
            raise TypeError('leaf pair must be set or tuple.')
        # iterate chord pitches if last leaf is chord
        for pair in pitchtools.list_unordered_named_pitch_pairs_in_expr(leaf_pair_list[1]):
            yield pair
