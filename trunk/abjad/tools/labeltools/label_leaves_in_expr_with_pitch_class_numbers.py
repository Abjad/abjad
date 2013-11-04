# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import iterationtools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.functiontools import attach


def label_leaves_in_expr_with_pitch_class_numbers(
    expr, 
    number=True, 
    color=False,
    markup_direction=Down,
    ):
    r'''Label leaves in `expr` with pitch-class numbers:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_pitch_class_numbers(staff)
        >>> print format(staff)
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 4 }
            f'8 _ \markup { \small 5 }
        }

    ::

        >>> show(staff) # doctest: +SKIP

    When ``color=True`` call
    :func:`~abjad.tools.labeltools.color_note_head_by_numbered_pitch_class_color_map`:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> labeltools.label_leaves_in_expr_with_pitch_class_numbers(
        ...     staff, color=True, number=False)
        >>> print format(staff)
        \new Staff {
            \once \override NoteHead #'color = #(x11-color 'red)
            c'8
            \once \override NoteHead #'color = #(x11-color 'orange)
            d'8
            \once \override NoteHead #'color = #(x11-color 'ForestGreen)
            e'8
            \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    You can set `number` and `color` at the same time.

    Returns none.
    '''
    from abjad.tools import labeltools

    for note in iterationtools.iterate_notes_in_expr(expr):
        if number:
            label = markuptools.MarkupCommand(
                'small', str(abs(note.written_pitch.numbered_pitch_class)))
            markup = markuptools.Markup(label, markup_direction)
            attach(markup, note)
        if color:
            labeltools.color_note_head_by_numbered_pitch_class_color_map(note)
