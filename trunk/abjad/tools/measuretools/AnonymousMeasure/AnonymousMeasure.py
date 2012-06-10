from abjad.tools.measuretools.DynamicMeasure.DynamicMeasure import DynamicMeasure


class AnonymousMeasure(DynamicMeasure):
    r'''.. versionadded:: 1.1

    Dynamic measure with no time signature::

        >>> measure = measuretools.AnonymousMeasure("c'8 d'8 e'8 f'8")

    ::

        >>> f(measure)
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

        >>> notes = [Note("c'8"), Note("d'8")]
        >>> measure.extend(notes)

    ::

        >>> f(measure)
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

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, music=None, **kwargs):
        DynamicMeasure.__init__(self, music=music, **kwargs)
        self.override.staff.time_signature.stencil = False
