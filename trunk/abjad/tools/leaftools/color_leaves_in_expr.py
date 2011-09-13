from abjad.tools.leaftools.color_leaf import color_leaf
from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def color_leaves_in_expr(expr, color):
    r""".. versionadded:: 2.0

    Color leaves in `expr`::

        abjad> staff = Staff([Note(1, (3, 16)), Rest((3, 16)), skiptools.Skip((3, 16)), Chord([0, 1, 9], (3, 16))])
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(cs'8., r8., s8., <c' cs' a'>8.)
        abjad> f(staff)
        \new Staff {
            cs'8. [
            r8.
            s8.
            <c' cs' a'>8. ]
        }

    ::

        abjad> leaftools.color_leaves_in_expr(staff, 'red')

    ::

        abjad> f(staff)
        \new Staff {
            \once \override Accidental #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            cs'8. [
            \once \override Dots #'color = #red
            \once \override Rest #'color = #red
            r8.
            s8.
            \once \override Accidental #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            <c' cs' a'>8. ]
        }

    Return none.
    """

    for leaf in iterate_leaves_forward_in_expr(expr):
        color_leaf(leaf, color)
