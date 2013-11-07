# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_leaf_numbers(expr, markup_direction=Down):
    r'''Label leaves in `expr` with leaf numbers:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_leaf_numbers(staff)
        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 1 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 3 }
            f'8 _ \markup { \small 4 }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Number leaves starting from ``1``.

    Returns none.
    '''

    for i, leaf in enumerate(iterate(expr).by_class(scoretools.Leaf)):
        leaf_number = i + 1
        label = markuptools.MarkupCommand('small', str(leaf_number))
        markup = markuptools.Markup(label, markup_direction)
        attach(markup, leaf)
