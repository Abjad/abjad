# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import override


def color_contents_of_container(container, color):
    r'''Color contents of `container`:

    ::

        >>> measure = Measure((2, 8), "c'8 d'8")

    ::

        >>> labeltools.color_contents_of_container(measure, 'red')
        Measure((2, 8), "c'8 d'8")

    ..  doctest::

        >>> print format(measure)
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

    ::

        >>> show(measure) # doctest: +SKIP

    Returns none.
    '''

    override(container).accidental.color = color
    override(container).beam.color = color
    override(container).dots.color = color
    override(container).note_head.color = color
    override(container).rest.color = color
    override(container).stem.color = color
    override(container).tuplet_bracket.color = color
    override(container).tuplet_number.color = color

    return container
