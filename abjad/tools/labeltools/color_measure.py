# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import override


def color_measure(measure, color='red'):
    r'''Color `measure` with `color`:

    ::

        >>> measure = Measure((2, 8), "c'8 d'8")

    ..  doctest::

        >>> print format(measure)
        {
            \time 2/8
            c'8
            d'8
        }

    ::

        >>> show(measure) # doctest: +SKIP

    ::

        >>> labeltools.color_measure(measure, 'red')
        Measure((2, 8), "c'8 d'8")

    ..  doctest::

        >>> print format(measure)
        {
            \override Beam #'color = #red
            \override Dots #'color = #red
            \override NoteHead #'color = #red
            \override Staff.TimeSignature #'color = #red
            \override Stem #'color = #red
            \time 2/8
            c'8
            d'8
            \revert Beam #'color
            \revert Dots #'color
            \revert NoteHead #'color
            \revert Staff.TimeSignature #'color
            \revert Stem #'color
        }

    ::

        >>> show(measure) # doctest: +SKIP

    Returns colored `measure`.

    Color names appear in LilyPond Learning Manual appendix B.5.
    '''

    # check measure type
    if not isinstance(measure, scoretools.Measure):
        message = 'must be measure: {}'
        message = message.format(measure)
        raise TypeError(message)

    # color measure
    override(measure).beam.color = color
    override(measure).dots.color = color
    override(measure).staff.time_signature.color = color
    override(measure).note_head.color = color
    override(measure).stem.color = color

    # return measure
    return measure
