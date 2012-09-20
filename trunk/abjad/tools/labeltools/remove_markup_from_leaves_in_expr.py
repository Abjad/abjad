from abjad.tools import iterationtools
from abjad.tools import markuptools


def remove_markup_from_leaves_in_expr(expr):
    r'''.. versionadded:: 1.1

    Remove markup from leaves in `expr`::

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

        >>> labeltools.remove_markup_from_leaves_in_expr(staff)
        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``label.clear_leaves()`` to
        ``labeltools.remove_markup_from_leaves_in_expr()``.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        for markup in markuptools.get_markup_attached_to_component(leaf):
            markup()
