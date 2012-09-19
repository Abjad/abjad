from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label pitch-classes of every vertical moment in `expr`::

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

        >>> labeltools.label_vertical_moments_in_expr_with_numbered_chromatic_pitch_classes(
        ...     score)

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
                                    7
                                    2
                                    0
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    5
                                    0
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
                                    5
                                    4
                                    0
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
                                    7
                                    0
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
        pitch_classes = [abs(pitch.numbered_chromatic_pitch_class) for pitch in pitches]
        pitch_classes = list(set(pitch_classes))
        pitch_classes.sort()
        pitch_classes.reverse()
        pitch_classes = ' '.join([str(x) for x in pitch_classes])
        pitch_classes = r'\small \column { %s }' % pitch_classes
        markuptools.Markup(pitch_classes, markup_direction)(vertical_moment.start_leaves[-1])
