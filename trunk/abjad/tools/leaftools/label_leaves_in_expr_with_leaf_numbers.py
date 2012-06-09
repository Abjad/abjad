from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_leaf_numbers(expr, markup_direction='down'):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with leaf numbers::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> leaftools.label_leaves_in_expr_with_leaf_numbers(staff)
        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 1 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 3 }
            f'8 _ \markup { \small 4 }
        }

    Number leaves starting from ``1``.

    .. versionchanged:: 2.0
        renamed ``label.leaf_numbers()`` to
        ``leaftools.label_leaves_in_expr_with_leaf_numbers()``.

    Return none.
    '''
    from abjad.tools import markuptools

    for i, leaf in enumerate(iterate_leaves_forward_in_expr(expr)):
        leaf_number = i + 1
        #label = r'\small %s' % leaf_number
        label = markuptools.MarkupCommand('small', str(leaf_number))
        markuptools.Markup(label, markup_direction)(leaf)
