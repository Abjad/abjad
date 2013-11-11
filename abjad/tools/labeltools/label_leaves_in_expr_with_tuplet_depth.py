# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_tuplet_depth(expr, markup_direction=Down):
    r'''Label leaves in `expr` with tuplet depth:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        >>> scoretools.FixedDurationTuplet(Duration(2, 8), staff[-3:])
        FixedDurationTuplet(1/4, [e'8, f'8, g'8])
        >>> labeltools.label_leaves_in_expr_with_tuplet_depth(staff)
        >>> print format(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 0 }
            \times 2/3 {
                e'8 _ \markup { \small 1 }
                f'8 _ \markup { \small 1 }
                g'8 _ \markup { \small 1 }
            }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for leaf in iterate(expr).by_class(scoretools.Leaf):
        label = markuptools.MarkupCommand(
            'small', str(leaf._get_parentage().tuplet_depth))
        markup = markuptools.Markup(label, markup_direction)
        attach(markup, leaf)
