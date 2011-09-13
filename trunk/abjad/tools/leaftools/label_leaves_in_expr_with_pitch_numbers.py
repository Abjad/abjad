from abjad.tools import pitchtools
from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_pitch_numbers(expr, markup_direction = 'down'):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with pitch numbers::

        abjad> staff = Staff(leaftools.make_leaves([None, 12, [13, 14, 15], None], [(1, 4)]))
        abjad> leaftools.label_leaves_in_expr_with_pitch_numbers(staff)
        abjad> f(staff)
        \new Staff {
            r4
            c''4 _ \markup { \small 12 }
            <cs'' d'' ef''>4 _ \markup { \column { \small 15 \small 14 \small 13 } }
            r4
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``label.leaf_pitch_numbers()`` to
        ``leaftools.label_leaves_in_expr_with_pitch_numbers()``.
    '''
    from abjad.tools import markuptools

    for leaf in iterate_leaves_forward_in_expr(expr):
        for pitch in reversed(pitchtools.list_named_chromatic_pitches_in_expr(leaf)):
            if pitch is not None:
                pitch_number = r'\small %s' % pitch.chromatic_pitch_number
                markuptools.Markup(pitch_number, markup_direction)(leaf)
