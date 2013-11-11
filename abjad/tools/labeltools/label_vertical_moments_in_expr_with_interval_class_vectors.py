# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_vertical_moments_in_expr_with_interval_class_vectors(
    expr, markup_direction=Down):
    r'''Label interval-class vector of every vertical moment in `expr`:

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

    ..  doctest::

        >>> print format(score)
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

    ::

        >>> show(score) # doctest: +SKIP

    Returns none.
    '''

    for vertical_moment in \
        iterate(expr).by_vertical_moment():
        leaves = vertical_moment.leaves
        pitches = pitchtools.PitchSegment.from_selection(leaves)
        if not pitches:
            continue
        interval_class_vector = \
            pitchtools.numbered_inversion_equivalent_interval_class_dictionary(
            pitches)
        formatted = _format_interval_class_vector(interval_class_vector)
        markup = markuptools.Markup(formatted, markup_direction)
        attach(markup, vertical_moment.start_leaves[-1])


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
