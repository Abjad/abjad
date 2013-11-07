# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import markuptools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_leaf_depth(expr, markup_direction=Down):
    r'''Label leaves in `expr` with leaf depth:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        >>> scoretools.FixedDurationTuplet(Duration(2, 8), staff[-3:])
        FixedDurationTuplet(1/4, [e'8, f'8, g'8])

    ::

        >>> labeltools.label_leaves_in_expr_with_leaf_depth(staff)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 1 }
            d'8 _ \markup { \small 1 }
            \times 2/3 {
                e'8 _ \markup { \small 2 }
                f'8 _ \markup { \small 2 }
                g'8 _ \markup { \small 2 }
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for leaf in iterate(expr).by_class(scoretools.Leaf):
        label = markuptools.MarkupCommand(
            'small', str(leaf._get_parentage().depth))
        markup = markuptools.Markup(label, markup_direction)
        attach(markup, leaf)
