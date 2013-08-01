# -*- encoding: utf-8 -*-
def label_leaves_in_expr_with_written_leaf_duration(
    expr, markup_direction=Down):
    r'''Label leaves in `expr` with writen leaf duration:

    ::

        >>> tuplet = Tuplet((2, 3), "c'8 d'8 e'8")
        >>> labeltools.label_leaves_in_expr_with_leaf_durations(tuplet)
        >>> f(tuplet)
        \times 2/3 {
            c'8 _ \markup { \column { \small 1/8 \small 1/12 } }
            d'8 _ \markup { \column { \small 1/8 \small 1/12 } }
            e'8 _ \markup { \column { \small 1/8 \small 1/12 } }
        }

    ::

        >>> show(tuplet) # doctest: +SKIP

    Return none.
    '''
    from abjad.tools import labeltools

    return labeltools.label_leaves_in_expr_with_leaf_durations(
        expr,
        label_durations=False,
        label_written_durations=True,
        markup_direction=markup_direction,
        )
