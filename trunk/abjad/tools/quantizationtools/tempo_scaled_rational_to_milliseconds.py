from abjad import Fraction
from abjad.tools.contexttools import TempoMark
from abjad.tools.durationtools import Duration


def tempo_scaled_rational_to_milliseconds(rational, tempo):
    '''Return the millisecond value of `rational` at `tempo`.

    ::

        abjad> from abjad.tools.quantizationtools import tempo_scaled_rational_to_milliseconds
        abjad> tempo = contexttools.TempoMark((1, 4), 60)
        abjad> tempo_scaled_rational_to_milliseconds(Fraction(1, 4), tempo)
        Duration(1000, 1)

    Return a :py:class:`~abjad.tools.durationtools.Duration`.
    '''

    assert isinstance(rational, (int, Fraction))
    assert isinstance(tempo, TempoMark)

    whole_note_duration = 1000 \
        * Fraction(tempo.duration.denominator, tempo.duration.numerator) \
        * Fraction(60, tempo.units_per_minute)

    return Duration(rational * whole_note_duration)
