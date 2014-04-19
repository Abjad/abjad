# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.topleveltools import override


def color_chord_note_heads_in_expr_by_pitch_class_color_map(chord, color_map):
    r'''Color `chord` note heads by pitch-class `color_map`:

    ::

        >>> chord = Chord([12, 14, 18, 21, 23], (1, 4))

    ::

        >>> pitches = [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
        >>> colors = ['red', 'blue', 'green']
        >>> color_map = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    ::

        >>> labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(chord, color_map)
        Chord("<c'' d'' fs'' a'' b''>4")

    ..  doctest::

        >>> print(format(chord))
        <
            \tweak #'color #red
            c''
            \tweak #'color #red
            d''
            \tweak #'color #green
            fs''
            \tweak #'color #green
            a''
            \tweak #'color #blue
            b''
        >4

    ::

        >>> show(chord) # doctest: +SKIP

    Also works on notes:

    ::

        >>> note = Note("c'4")

    ::

        >>> labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(note, color_map)
        Note("c'4")

    ..  doctest::

        >>> print(format(note))
        \once \override NoteHead #'color = #red
        c'4

    ::

        >>> show(note) # doctest: +SKIP

    When `chord` is neither a chord nor note return `chord` unchanged:

    ::

        >>> staff = Staff([])

    ::

        >>> labeltools.color_chord_note_heads_in_expr_by_pitch_class_color_map(staff, color_map)
        Staff()

    Return `chord`.
    '''

    if isinstance(chord, scoretools.Chord):
        for note_head in chord.note_heads:
            pc = note_head.written_pitch.numbered_pitch_class
            color = color_map.get(pc, None)
            if color is not None:
                note_head.tweak.color = color
    elif isinstance(chord, scoretools.Note):
        note = chord
        note_head = note.note_head
        pc = note_head.written_pitch.numbered_pitch_class
        color = color_map.get(pc, None)
        if color is not None:
            override(note).note_head.color = color

    return chord
