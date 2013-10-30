# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.scoretools import attach


def label_leaves_in_expr_with_pitch_numbers(expr, markup_direction=Down):
    r'''Label leaves in `expr` with pitch numbers:

    ::

        >>> staff = Staff(scoretools.make_leaves([None, 12, [13, 14, 15], None], [(1, 4)]))
        >>> labeltools.label_leaves_in_expr_with_pitch_numbers(staff)
        >>> f(staff)
        \new Staff {
            r4
            c''4 _ \markup { \small 12 }
            <cs'' d'' ef''>4 _ \markup { \column { \small 15 \small 14 \small 13 } }
            r4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        for pitch in reversed(pitchtools.PitchSegment.from_selection(leaf)):
            if pitch is not None:
                label = markuptools.MarkupCommand('small', str(pitch.pitch_number))
                markup = markuptools.Markup(label, markup_direction)
                attach(markup, leaf)
