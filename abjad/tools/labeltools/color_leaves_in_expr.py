# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import iterate


def color_leaves_in_expr(expr, color):
    r"""Color leaves in `expr`:

    ::

        >>> staff = Staff("cs'8. [ r8. s8. <c' cs' a'>8. ]")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            cs'8. [
            r8.
            s8.
            <c' cs' a'>8. ]
        }

    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> labeltools.color_leaves_in_expr(staff, 'red')

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \once \override Accidental #'color = #red
            \once \override Beam #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            \once \override Stem #'color = #red
            cs'8. [
            \once \override Dots #'color = #red
            \once \override Rest #'color = #red
            r8.
            s8.
            \once \override Accidental #'color = #red
            \once \override Beam #'color = #red
            \once \override Dots #'color = #red
            \once \override NoteHead #'color = #red
            \once \override Stem #'color = #red
            <c' cs' a'>8. ]
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    """
    from abjad.tools import labeltools

    for leaf in iterate(expr).by_class(scoretools.Leaf):
        labeltools.color_leaf(leaf, color)
