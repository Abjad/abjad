from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_pitch_numbers(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label pitch numbers of every vertical moment in `expr`::

        >>> from abjad.tools import verticalitytools

    ::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "alto" g4 f4""")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "bass" c,2""")
        >>> score.append(staff)

    ::

        >>> labeltools.label_vertical_moments_in_expr_with_pitch_numbers(score)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \small
                            \column
                                {
                                    2
                                    -5
                                    -24
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    5
                                    -7
                                    -24
                                }
                        }
            }
            \new Staff {
                \clef "alto"
                g4
                f4
                    _ \markup {
                        \small
                            \column
                                {
                                    4
                                    -7
                                    -24
                                }
                        }
            }
            \new Staff {
                \clef "bass"
                c,2
                    _ \markup {
                        \small
                            \column
                                {
                                    0
                                    -5
                                    -24
                                }
                        }
            }
        >>

    Return none.
    '''

    for vertical_moment in verticalitytools.iterate_vertical_moments_in_expr(expr):
        leaves = vertical_moment.leaves
        pitches = pitchtools.list_named_chromatic_pitches_in_expr(leaves)
        if not pitches:
            continue
        pitch_numbers = [abs(pitch.numbered_chromatic_pitch) for pitch in pitches]
        pitch_numbers = ' '.join([str(x) for x in pitch_numbers])
        pitch_numbers = r'\small \column { %s }' % pitch_numbers
        markuptools.Markup(pitch_numbers, markup_direction)(vertical_moment.start_leaves[-1])
