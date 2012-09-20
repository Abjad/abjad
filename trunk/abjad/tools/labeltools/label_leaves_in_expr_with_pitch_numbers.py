from abjad.tools import iterationtools
from abjad.tools import markuptools
from abjad.tools import pitchtools


def label_leaves_in_expr_with_pitch_numbers(expr, markup_direction=Down):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with pitch numbers::

        >>> staff = Staff(leaftools.make_leaves([None, 12, [13, 14, 15], None], [(1, 4)]))
        >>> labeltools.label_leaves_in_expr_with_pitch_numbers(staff)
        >>> f(staff)
        \new Staff {
            r4
            c''4 _ \markup { \small 12 }
            <cs'' d'' ef''>4 _ \markup { \column { \small 15 \small 14 \small 13 } }
            r4
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``label.leaf_pitch_numbers()`` to
        ``labeltools.label_leaves_in_expr_with_pitch_numbers()``.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        for pitch in reversed(pitchtools.list_named_chromatic_pitches_in_expr(leaf)):
            if pitch is not None:
                label = markuptools.MarkupCommand('small', str(pitch.chromatic_pitch_number))
                markuptools.Markup(label, markup_direction)(leaf)
