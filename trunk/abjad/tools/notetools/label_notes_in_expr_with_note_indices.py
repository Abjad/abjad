from abjad.tools import markuptools
from abjad.tools.notetools.iterate_notes_forward_in_expr import iterate_notes_forward_in_expr


def label_notes_in_expr_with_note_indices(expr, markup_direction = 'down'):
    r'''.. versionadded:: 2.0

    Label notes in `expr` with note indices::

        abjad> staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")

    ::

        abjad> notetools.label_notes_in_expr_with_note_indices(staff)

    ::

        abjad> f(staff)
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

    for i, note in enumerate(iterate_notes_forward_in_expr(expr)):
        label = r'\small %s' % i
        markuptools.Markup(label, markup_direction)(note)
