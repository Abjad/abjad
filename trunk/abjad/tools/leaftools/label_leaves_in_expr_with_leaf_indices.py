from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_leaf_indices(expr, markup_direction = 'down'):
    r'''.. versionadded:: 2.0

    Label leaves in `expr` with leaf indices::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> leaftools.label_leaves_in_expr_with_leaf_indices(staff)
        abjad> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 1 }
            e'8 _ \markup { \small 2 }
            f'8 _ \markup { \small 3 }
        }

    Return none.
    '''
    from abjad.tools import markuptools

    for i, leaf in enumerate(iterate_leaves_forward_in_expr(expr)):
        label = r'\small %s' % i
        markuptools.Markup(label, markup_direction)(leaf)
