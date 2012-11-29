from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_chromatic_intervals(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label harmonic chromatic intervals of every vertical moment in `expr`::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "alto" g4 f4""")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "bass" c,2""")
        >>> score.append(staff)

    ::

        >>> labeltools.label_vertical_moments_in_expr_with_chromatic_intervals(
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
                                    26
                                    19
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    29
                                    17
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
                                    28
                                    17
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
                                    24
                                    19
                                }
                        }
            }
        >>

    ::

        >>> show(score) # doctest: +SKIP

    Return none.
    '''

    for vertical_moment in verticalitytools.iterate_vertical_moments_in_expr(expr):
        leaves = vertical_moment.leaves
        notes = [leaf for leaf in leaves if isinstance(leaf, notetools.Note)]
        if not notes:
            continue
        notes.sort(lambda x, y: cmp(x.written_pitch.numbered_chromatic_pitch,
            y.written_pitch.numbered_chromatic_pitch))
        notes.reverse()
        bass_note = notes[-1]
        upper_notes = notes[:-1]
        hcis = []
        for upper_note in upper_notes:
            hci = pitchtools.calculate_harmonic_chromatic_interval(
                bass_note, upper_note)
            hcis.append(hci)
        hcis = ' '.join([str(hci) for hci in hcis])
        hcis = r'\small \column { %s }' % hcis
        markuptools.Markup(hcis, markup_direction)(vertical_moment.start_leaves[-1])
