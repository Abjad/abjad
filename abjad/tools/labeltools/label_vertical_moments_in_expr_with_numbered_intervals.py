# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_vertical_moments_in_expr_with_numbered_intervals(
    expr, markup_direction=Down):
    r'''Label numbered intervals of every vertical moment in `expr`:

    ::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "alto" g4 f4""")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "bass" c,2""")
        >>> score.append(staff)

    ::

        >>> labeltools.label_vertical_moments_in_expr_with_numbered_intervals(
        ...     score)

    ..  doctest::

        >>> print(format(score))
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \small
                            \column
                                {
                                    +26
                                    +19
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    +29
                                    +17
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
                                    +28
                                    +17
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
                                    +24
                                    +19
                                }
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
        notes = [leaf for leaf in leaves if isinstance(leaf, scoretools.Note)]
        if not notes:
            continue
        notes.sort(key=lambda x: x.written_pitch.numbered_pitch)
        notes.reverse()
        bass_note = notes[-1]
        upper_notes = notes[:-1]
        intervals = []
        for upper_note in upper_notes:
            interval = pitchtools.NumberedInterval.from_pitch_carriers(
                bass_note, upper_note)
            intervals.append(interval)
        markup = markuptools.Markup(
            r'\small \column {{ {} }}'.format(
                ' '.join(str(interval)
                    for interval in intervals)),
            markup_direction,
            )
        attach(markup, vertical_moment.start_leaves[-1])
