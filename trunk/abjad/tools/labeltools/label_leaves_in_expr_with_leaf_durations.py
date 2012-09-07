def label_leaves_in_expr_with_leaf_durations(expr, markup_direction=Down):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with leaf durations::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8")
        >>> labeltools.label_leaves_in_expr_with_leaf_durations(tuplet)
        >>> f(tuplet)
        \times 2/3 {
            c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
            d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
            e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        }

    Label both written duration and prolated duration.

    Return none.
    '''
    from abjad.tools.labeltools._label_leaves_in_expr_with_leaf_durations import \
        _label_leaves_in_expr_with_leaf_durations

    show = ['written', 'prolated']
    return _label_leaves_in_expr_with_leaf_durations(expr, markup_direction=markup_direction, show=show)
