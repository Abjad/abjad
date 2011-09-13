from abjad.tools.measuretools.Measure import Measure


def color_measure(measure, color = 'red'):
    r'''.. versionadded:: 2.0

    Color `measure` with `color`::

        abjad> measure = Measure((2, 8), "c'8 d'8")

    ::

        abjad> f(measure)
        {
            \time 2/8
            c'8
            d'8
        }

    ::

        abjad> measuretools.color_measure(measure, 'red')
        Measure(2/8, [c'8, d'8])

    ::

        abjad> f(measure)
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

    Return colored `measure`.

    Color names appear in LilyPond Learning Manual appendix B.5.
    '''

    # check measure type
    if not isinstance(measure, Measure):
        raise TypeError('must be measure: %s' % measure)

    # color measure
    measure.override.beam.color = color
    measure.override.dots.color = color
    measure.override.staff.time_signature.color = color
    measure.override.note_head.color = color
    measure.override.stem.color = color

    # return measure
    return measure
