from abjad.tools import sequencetools


def iterate_named_chromatic_pitch_pairs_forward_in_expr(expr):
    r'''.. versionadded:: 2.0

    Iterate left-to-right, top-to-bottom named chromatic pitch pairs in `expr`::

        abjad> score = Score([])
        abjad> notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'4")]
        abjad> score.append(Staff(notes))
        abjad> notes = [Note(x, (1, 4)) for x in [-12, -15, -17]]
        abjad> score.append(Staff(notes))
        abjad> contexttools.ClefMark('bass')(score[1])
        ClefMark('bass')(Staff{3})

    ::

        abjad> f(score)
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

        abjad> for pair in pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr(score):
        ...     pair
        ...
        (NamedChromaticPitch("c'"), NamedChromaticPitch('c'))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("d'"))
        (NamedChromaticPitch('c'), NamedChromaticPitch("d'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("e'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch('a,'))
        (NamedChromaticPitch('c'), NamedChromaticPitch("e'"))
        (NamedChromaticPitch('c'), NamedChromaticPitch('a,'))
        (NamedChromaticPitch("e'"), NamedChromaticPitch('a,'))
        (NamedChromaticPitch("e'"), NamedChromaticPitch("f'"))
        (NamedChromaticPitch('a,'), NamedChromaticPitch("f'"))
        (NamedChromaticPitch("f'"), NamedChromaticPitch("g'"))
        (NamedChromaticPitch("f'"), NamedChromaticPitch('g,'))
        (NamedChromaticPitch('a,'), NamedChromaticPitch("g'"))
        (NamedChromaticPitch('a,'), NamedChromaticPitch('g,'))
        (NamedChromaticPitch("g'"), NamedChromaticPitch('g,'))

    Chords are handled correctly. ::

        abjad> chord_1 = Chord([0, 2, 4], (1, 4))
        abjad> chord_2 = Chord([17, 19], (1, 4))
        abjad> staff = Staff([chord_1, chord_2])

    ::

        abjad> f(staff)
        \new Staff {
            <c' d' e'>4
            <f'' g''>4
        }

    ::

        abjad> for pair in pitchtools.iterate_named_chromatic_pitch_pairs_forward_in_expr(staff):
        ...   print pair
        (NamedChromaticPitch("c'"), NamedChromaticPitch("d'"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("e'"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("e'"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("f''"))
        (NamedChromaticPitch("c'"), NamedChromaticPitch("g''"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("f''"))
        (NamedChromaticPitch("d'"), NamedChromaticPitch("g''"))
        (NamedChromaticPitch("e'"), NamedChromaticPitch("f''"))
        (NamedChromaticPitch("e'"), NamedChromaticPitch("g''"))
        (NamedChromaticPitch("f''"), NamedChromaticPitch("g''"))

    Return generator.
    '''
    from abjad.tools.leaftools.iterate_leaf_pairs_forward_in_expr import iterate_leaf_pairs_forward_in_expr

    from abjad.tools import pitchtools
    for leaf_pair in iterate_leaf_pairs_forward_in_expr(expr):
        leaf_pair_list = list(leaf_pair)
        # iterate chord pitches if first leaf is chord
        for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair_list[0]):
            yield pair
        if isinstance(leaf_pair, set):
            for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair):
                yield pair
        elif isinstance(leaf_pair, tuple):
            for pair in pitchtools.list_ordered_named_chromatic_pitch_pairs_from_expr_1_to_expr_2(*leaf_pair):
                yield pair
        else:
            raise TypeError('leaf pair must be set or tuple.')
        # iterate chord pitches if last leaf is chord
        for pair in pitchtools.list_unordered_named_chromatic_pitch_pairs_in_expr(leaf_pair_list[1]):
            yield pair
