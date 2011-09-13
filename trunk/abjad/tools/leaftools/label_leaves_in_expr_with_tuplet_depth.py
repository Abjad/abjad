from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_tuplet_depth(expr, markup_direction = 'down'):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with tuplet depth::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        abjad> tuplettools.FixedDurationTuplet(Duration(2, 8), staff[-3:])
        FixedDurationTuplet(1/4, [e'8, f'8, g'8])
        abjad> leaftools.label_leaves_in_expr_with_tuplet_depth(staff)
        abjad> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 0 }
            \times 2/3 {
                e'8 _ \markup { \small 1 }
                f'8 _ \markup { \small 1 }
                g'8 _ \markup { \small 1 }
            }
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``label.leaf_depth_tuplet()`` to
        ``leaftools.label_leaves_in_expr_with_tuplet_depth()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import markuptools

    for leaf in iterate_leaves_forward_in_expr(expr):
        label = r'\small %s' % componenttools.component_to_tuplet_depth(leaf)
        markuptools.Markup(label, markup_direction)(leaf)
