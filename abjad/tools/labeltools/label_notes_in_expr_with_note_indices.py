# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_notes_in_expr_with_note_indices(expr, markup_direction=Down):
    r'''Label notes in `expr` with note indices:

    ::

        >>> staff = Staff("c'8 d'8 r8 r8 g'8 a'8 r8 c''8")

    ::

        >>> labeltools.label_notes_in_expr_with_note_indices(staff)

    ..  doctest::

        >>> print format(staff)
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

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''

    for i, note in enumerate(iterate(expr).by_class(scoretools.Note)):
        label = r'\small %s' % i
        markup = markuptools.Markup(label, markup_direction)
        attach(markup, note)
