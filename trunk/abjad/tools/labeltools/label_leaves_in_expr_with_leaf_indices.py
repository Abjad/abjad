# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import markuptools


def label_leaves_in_expr_with_leaf_indices(expr, markup_direction=Down):
    r'''Label leaves in `expr` with leaf indices:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_leaf_indices(staff)
        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 1 }
            e'8 _ \markup { \small 2 }
            f'8 _ \markup { \small 3 }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for i, leaf in enumerate(iterationtools.iterate_leaves_in_expr(expr)):
        label = markuptools.MarkupCommand('small', str(i))
        markup = markuptools.Markup(label, markup_direction)
        markup.attach(leaf)
