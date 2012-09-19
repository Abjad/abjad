from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_chromatic_interval_classes(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label harmonic chromatic interval-classes of every vertical moment in `expr`::

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

        >>> labeltools.label_vertical_moments_in_expr_with_chromatic_interval_classes(
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
                                    2
                                    7
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    5
                                    5
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
                                    5
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
                                    12
                                    7
                                }
                        }
            }
        >>

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
        hcics = []
        for upper_note in upper_notes:
            hcic = \
                pitchtools.calculate_harmonic_chromatic_interval_class(
                bass_note, upper_note)
            hcics.append(hcic)
        hcics = ' '.join([str(hcic) for hcic in hcics])
        hcics = r'\small \column { %s }' % hcics
        markuptools.Markup(hcics, markup_direction)(vertical_moment.start_leaves[-1])
