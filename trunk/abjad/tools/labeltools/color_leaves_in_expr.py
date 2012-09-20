from abjad.tools import iterationtools


def color_leaves_in_expr(expr, color):
    r""".. versionadded:: 2.0

    Color leaves in `expr`::

        >>> staff = Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")
        
    ::

        >>> f(staff)
        \new Staff {
            cs'8. [
            r8.
            s8.
            <c' cs' a'>8. ]
        }

    ::

        >>> labeltools.color_leaves_in_expr(staff, 'red')

    ::

        >>> f(staff)
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
    from abjad.tools import labeltools

    for leaf in iterationtools.iterate_leaves_in_expr(expr):
        labeltools.color_leaf(leaf, color)
