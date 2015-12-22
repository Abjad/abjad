# -*- coding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def label_leaves_in_expr_with_pitch_class_numbers(
    expr,
    number=True,
    color=False,
    direction=Down,
    ):
    r'''Labels leaves in `expr` with pitch-class numbers.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_pitch_class_numbers(staff)
        >>> print(format(staff))
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 4 }
            f'8 _ \markup { \small 5 }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Returns none.
    '''
    from abjad.tools import labeltools

    for note in iterate(expr).by_class(scoretools.Note):
        if number:
            label = markuptools.MarkupCommand(
                'small',
                str(note.written_pitch.numbered_pitch_class.pitch_class_number)
                )
            markup = markuptools.Markup(label, direction)
            attach(markup, note)