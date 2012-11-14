from abjad.tools import contexttools
from abjad.tools import durationtools


def tempo_scaled_rational_to_milliseconds(rational, tempo):
    '''Return the millisecond value of `rational` at `tempo`.

    ::

        >>> rational = (1, 4)
        >>> tempo = contexttools.TempoMark((1, 4), 60)
        >>> quantizationtools.tempo_scaled_rational_to_milliseconds(
        ...     rational, tempo)
        Duration(1000, 1)

    Return ``Duration`` instance.
    '''

    duration = durationtools.Duration(rational)
    tempo = contexttools.TempoMark(tempo)

    whole_note_duration = 1000 \
        * durationtools.Multiplier(tempo.duration.denominator, tempo.duration.numerator) \
        * durationtools.Multiplier(60, tempo.units_per_minute)

    return durationtools.Duration(duration * whole_note_duration)
