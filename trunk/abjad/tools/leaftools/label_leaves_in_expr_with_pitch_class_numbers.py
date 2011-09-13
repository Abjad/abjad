from abjad.tools import componenttools


def label_leaves_in_expr_with_pitch_class_numbers(expr, number = True, color = False,
    markup_direction = 'down'):
    r'''.. versionadded:: 1.1

    Label leaves in `expr` with pitch-class numbers::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(t)
        abjad> print t.format
        \new Staff {
            c'8 _ \markup { \small 0 }
            d'8 _ \markup { \small 2 }
            e'8 _ \markup { \small 4 }
            f'8 _ \markup { \small 5 }
        }

    When ``color = True`` call :func:`~abjad.tools.notetools.color_note_head_by_numbered_chromatic_pitch_class_color_map`.

    ::

        abjad> t = Staff("c'8 d'8 e'8 f'8")
        abjad> leaftools.label_leaves_in_expr_with_pitch_class_numbers(t, color = True, number = False)
        abjad> print t.format
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

    You can set `number` and `color` at the same time.

    .. versionchanged:: 2.0
        renamed ``label.leaf_pcs()`` to
        ``leaftools.label_leaves_in_expr_with_pitch_class_numbers()``.

    Return none.
    '''
    from abjad.tools import markuptools
    from abjad.tools import notetools
    from abjad.tools.notetools.Note import Note

    for note in componenttools.iterate_components_forward_in_expr(expr, Note):
        if number:
            label = r'\small %s' % abs(note.written_pitch.numbered_chromatic_pitch_class)
            markuptools.Markup(label, markup_direction)(note)
        if color:
            notetools.color_note_head_by_numbered_chromatic_pitch_class_color_map(note)
