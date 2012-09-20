from abjad.tools import componenttools
from abjad.tools import iterationtools
from abjad.tools import markuptools


def label_leaves_in_expr_with_leaf_depth(expr, markup_direction=Down):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with leaf depth::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8")
        >>> tuplettools.FixedDurationTuplet(Duration(2, 8), staff[-3:])
        FixedDurationTuplet(1/4, [e'8, f'8, g'8])
        >>> labeltools.label_leaves_in_expr_with_leaf_depth(staff)
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

    .. versionchanged:: 2.0
        renamed ``label.leaf_depth()`` to
        ``labeltools.label_leaves_in_expr_with_leaf_depth()``.

    Return none.
    '''

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        label = markuptools.MarkupCommand('small', str(componenttools.component_to_score_depth(leaf)))
        markuptools.Markup(label, markup_direction)(leaf)
