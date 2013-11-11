# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_vertical_moments_in_expr_with_numbered_interval_classes(
    expr, markup_direction=Down):
    r'''Label numbered interval-classes of every vertical 
    moment in `expr`:

    ::

        >>> score = Score([])
        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "alto" g4 f4""")
        >>> score.append(staff)
        >>> staff = Staff(r"""\clef "bass" c,2""")
        >>> score.append(staff)

    ::

        >>> labeltools.label_vertical_moments_in_expr_with_numbered_interval_classes(
        ...     score)

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \small
                            \column
                                {
                                    +2
                                    +7
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    +5
                                    +5
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
                                    +4
                                    +5
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
                                    +12
                                    +7
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
        interval_classes = []
        for upper_note in upper_notes:
            interval_class = \
                pitchtools.NumberedIntervalClass.from_pitch_carriers(
                bass_note, upper_note)
            interval_classes.append(interval_class)
        markup = markuptools.Markup(
            r'\small \column {{ {} }}'.format(
                ' '.join(str(interval_class) 
                    for interval_class in interval_classes)),
            markup_direction,
            )
        attach(markup, vertical_moment.start_leaves[-1])
