def label_tie_chains_in_expr_with_prolated_tie_chain_duration(expr, markup_direction=Down):
    r'''Label tie chains in `expr` with prolated tie chain duration::

        >>> staff = Staff(r"\times 2/3 { c'8 ~ c'8 c'8 ~ } c'8")
        >>> labeltools.label_tie_chains_in_expr_with_prolated_tie_chain_duration(staff)

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 ~
                    _ \markup {
                        \small
                            1/6
                        }
                c'8
                c'8 ~
                    _ \markup {
                        \small
                            5/24
                        }
            }
            c'8
        }

    Return none.
    '''
    from abjad.tools.labeltools._label_leaves_in_expr_with_leaf_durations import \
        _label_leaves_in_expr_with_leaf_durations

    show = ['prolated']
    return _label_leaves_in_expr_with_leaf_durations(
        expr, markup_direction=markup_direction, show=show, ties='together')
