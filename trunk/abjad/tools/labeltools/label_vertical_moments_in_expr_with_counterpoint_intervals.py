from abjad.tools import markuptools
from abjad.tools import notetools
from abjad.tools import pitchtools
from abjad.tools import verticalitytools


def label_vertical_moments_in_expr_with_counterpoint_intervals(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label counterpoint interval of every vertical moment in `expr`::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "alto" g4 f4""")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "bass" c,2""")
        >>> score.append(staff)

    ::

        >>> labeltools.label_vertical_moments_in_expr_with_counterpoint_intervals(score)

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
                                    5
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    4
                                    4
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
                                    3
                                    4
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
                                    8
                                    5
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
        melodic_diatonic_intervals = []
        for upper_note in upper_notes:
            diatonic_interval = pitchtools.calculate_melodic_diatonic_interval(
                bass_note.written_pitch, upper_note.written_pitch)
            melodic_diatonic_intervals.append(diatonic_interval)
        intervals = melodic_diatonic_intervals
        hcpics = []
        for mdi in melodic_diatonic_intervals:
            hcpic = pitchtools.HarmonicCounterpointIntervalClass(mdi)
            hcpics.append(hcpic)
        intervals = ' '.join([str(x) for x in hcpics])
        intervals = r'\small \column { %s }' % intervals
        markuptools.Markup(intervals, markup_direction)(vertical_moment.start_leaves[-1])
