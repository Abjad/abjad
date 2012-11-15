from abjad.tools import contexttools
from abjad.tools import durationtools


def tempo_scaled_duration_to_milliseconds(duration, tempo):
    '''Return the millisecond value of `duration` at `tempo`.

    ::

        >>> duration = (1, 4)
        >>> tempo = contexttools.TempoMark((1, 4), 60)
        >>> quantizationtools.tempo_scaled_duration_to_milliseconds(
        ...     duration, tempo)
        Duration(1000, 1)

    Return ``Duration`` instance.
    '''

    duration = durationtools.Duration(duration)
    tempo = contexttools.TempoMark(tempo)

    whole_note_duration = 1000 \
        * durationtools.Multiplier(tempo.duration.denominator, tempo.duration.numerator) \
        * durationtools.Multiplier(60, tempo.units_per_minute)

    return durationtools.Duration(duration * whole_note_duration)
