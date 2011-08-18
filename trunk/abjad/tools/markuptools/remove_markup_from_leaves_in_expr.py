#from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def remove_markup_from_leaves_in_expr(expr):
    r'''.. versionadded:: 1.1

    Remove markup from leaves in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(staff)
        abjad> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 4 }
            f'8 _ \markup { \small 5 }
        }

    ::

        abjad> markuptools.remove_markup_from_leaves_in_expr(staff)
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``label.clear_leaves()`` to
        ``markuptools.remove_markup_from_leaves_in_expr()``.
    '''
    from abjad.tools import leaftools
    from abjad.tools import markuptools

    for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
        for markup in markuptools.get_markup_attached_to_component(leaf):
            markup()
