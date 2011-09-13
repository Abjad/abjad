from abjad.tools.durationtools.Duration import Duration


class Offset(Duration):
    '''.. versionadded:: 2.0

    Abjad model of offset value of musical time::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.Offset(121, 16)
        Offset(121, 16)

    Offset inherits from duration (which inherits from built-in ``Fraction``).
    '''

    pass
