# -*- encoding: utf-8 -*-
from abjad.tools import iterationtools
from abjad.tools import markuptools


def remove_markup_from_leaves_in_expr(expr):
    r'''Remove markup from leaves in `expr`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_pitch_class_numbers(staff)
        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 4 }
            f'8 _ \markup { \small 5 }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> labeltools.remove_markup_from_leaves_in_expr(staff)
        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        for markup in leaf._get_markup():
            markup()
