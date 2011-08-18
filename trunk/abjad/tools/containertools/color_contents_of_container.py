def color_contents_of_container(container, color):
    r'''.. versionadded:: 2.0

    Color contents of `container`::

        abjad> measure = Measure((2, 8), "c'8 d'8")

    ::

        abjad> containertools.color_contents_of_container(measure, 'red')
        Measure(2/8, [c'8, d'8])

    ::

        abjad> f(measure)
        {
            \override Accidental #'color = #red
            \override Beam #'color = #red
            \override Dots #'color = #red
            \override NoteHead #'color = #red
            \override Rest #'color = #red
            \override Stem #'color = #red
            \override TupletBracket #'color = #red
            \override TupletNumber #'color = #red
            \time 2/8
            c'8
            d'8
            \revert Accidental #'color
            \revert Beam #'color
            \revert Dots #'color
            \revert NoteHead #'color
            \revert Rest #'color
            \revert Stem #'color
            \revert TupletBracket #'color
            \revert TupletNumber #'color
        }

    Return none.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_color()`` to
        ``containertools.color_contents_of_container()``.
    '''

    container.override.accidental.color = color
    container.override.beam.color = color
    container.override.dots.color = color
    container.override.note_head.color = color
    container.override.rest.color = color
    container.override.stem.color = color
    container.override.tuplet_bracket.color = color
    container.override.tuplet_number.color = color

    return container
