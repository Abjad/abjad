from abjad.tools import markuptools
from abjad.tools import iterationtools


def label_notes_in_expr_with_note_indices(expr, markup_direction=Down):
    r'''.. versionadded:: 2.0

    Label notes in `expr` with note indices::

        >>> staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")

    ::

        >>> labeltools.label_notes_in_expr_with_note_indices(staff)

    ::

        >>> f(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 1 }
            r8
            r8
            g'8 _ \markup { \small 2 }
            a'8 _ \markup { \small 3 }
            r8
            c''8 _ \markup { \small 4 }
        }

    Return none.
    '''

    for i, note in enumerate(iterationtools.iterate_notes_in_expr(expr)):
        label = r'\small %s' % i
        markuptools.Markup(label, markup_direction)(note)
