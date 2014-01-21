# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_vertical_moments_in_expr_with_pitch_numbers(
    expr, markup_direction=Down):
    r'''Label pitch numbers of every vertical moment in `expr`:

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

    ..  doctest::

        >>> print format(score)
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

    ::

        >>> show(score) # doctest: +SKIP

    Returns none.
    '''

    for vertical_moment in iterate(expr).by_vertical_moment():
        leaves = vertical_moment.leaves
        pitches = pitchtools.PitchSegment.from_selection(leaves)
        if not pitches:
            continue
        pitch_numbers = [
            pitch.numbered_pitch.pitch_number 
            for pitch in pitches
            ]
        pitch_numbers = ' '.join([str(x) for x in pitch_numbers])
        pitch_numbers = r'\small \column { %s }' % pitch_numbers
        markup = markuptools.Markup(pitch_numbers, markup_direction)
        attach(markup, vertical_moment.start_leaves[-1])
