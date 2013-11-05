# -*- encoding: utf-8 -*-


def label_tie_chains_in_expr_with_written_tie_chain_duration(
    expr, markup_direction=Down):
    r'''Label tie chains in `expr` with written tie chain duration:

    ::

        >>> staff = Staff(r"\times 2/3 { c'8 ~ c'8 c'8 ~ } c'8")
        >>> labeltools.label_tie_chains_in_expr_with_written_tie_chain_duration(
        ...     staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 ~ _ \markup { \small 1/4 }
                c'8
                c'8 ~ _ \markup { \small 1/4 }
            }
            c'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''
    from abjad.tools import labeltools

    return labeltools.label_leaves_in_expr_with_leaf_durations(
        expr,
        label_durations=False,
        label_written_durations=True,
        markup_direction=markup_direction,
        )
