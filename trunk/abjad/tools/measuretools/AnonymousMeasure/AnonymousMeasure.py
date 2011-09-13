from abjad.tools.measuretools.DynamicMeasure.DynamicMeasure import DynamicMeasure


class AnonymousMeasure(DynamicMeasure):
    r'''.. versionadded:: 1.1

    Dynamic measure with no time signature::

        abjad> measure = measuretools.AnonymousMeasure("c'8 d'8 e'8 f'8")

    ::

        abjad> f(measure)
        {
            \override Staff.TimeSignature #'stencil = ##f
            \time 1/2
            c'8
            d'8
            e'8
            f'8
            \revert Staff.TimeSignature #'stencil
        }

    ::

        abjad> notes = [Note("c'8"), Note("d'8")]
        abjad> measure.extend(notes)

    ::

        abjad> f(measure)
        {
            \override Staff.TimeSignature #'stencil = ##f
            \time 3/4
            c'8
            d'8
            e'8
            f'8
            c'8
            d'8
            \revert Staff.TimeSignature #'stencil
        }

    Return anonymous measure.
    '''

    __slots__ = ()

    def __init__(self, music = None, **kwargs):
        DynamicMeasure.__init__(self, music = music, **kwargs)
        self.override.staff.time_signature.stencil = False
