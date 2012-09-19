from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_interval_class_vectors(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label interval-class vector of every vertical moment in `expr`::

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

        >>> labeltools.label_vertical_moments_in_expr_with_interval_class_vectors(score)

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \tiny
                            0010020
                        }
                e'8
                f'8
                    _ \markup {
                        \tiny
                            1000020
                        }
            }
            \new Staff {
                \clef "alto"
                g4
                f4
                    _ \markup {
                        \tiny
                            0100110
                        }
            }
            \new Staff {
                \clef "bass"
                c,2
                    _ \markup {
                        \tiny
                            1000020
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
        interval_class_vector = pitchtools.inversion_equivalent_chromatic_interval_class_number_dictionary(
            pitches)
        formatted = _format_interval_class_vector(interval_class_vector)
        markuptools.Markup(formatted, markup_direction)(vertical_moment.start_leaves[-1])


def _format_interval_class_vector(interval_class_vector):
    counts = []
    for i in range(7):
        counts.append(interval_class_vector[i])
    counts = ''.join([str(x) for x in counts])
    if len(interval_class_vector) == 13:
        quartertones = []
        for i in range(6):
            quartertones.append(interval_class_vector[i+0.5])
        quartertones = ''.join([str(x) for x in quartertones])
        return r'\tiny \column { "%s" "%s" }' % (counts, quartertones)
    else:
        return r'\tiny %s' % counts
