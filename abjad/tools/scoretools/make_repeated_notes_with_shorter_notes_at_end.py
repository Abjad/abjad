# -*- coding: utf-8 -*-
import fractions
from abjad.tools import durationtools
from abjad.tools import selectiontools


def make_repeated_notes_with_shorter_notes_at_end(
    pitch,
    written_duration,
    total_duration,
    prolation=1,
    ):
    r'''Makes repeated notes with `pitch` and `written_duration` summing to
    `total_duration` under `prolation`.

    ::

        >>> args = [0, Duration(1, 16), Duration(1, 4)]
        >>> notes = scoretools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'16
            c'16
            c'16
            c'16
        }

    Fill power-of-two remaining duration with power-of-two notes of lesser written duration:

    ::

        >>> args = [0, Duration(1, 16), Duration(9, 32)]
        >>> notes = scoretools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'32
        }

    Fill non-power-of-two remaining duration with ad hoc tuplet:

    ::

        >>> args = [0, Duration(1, 16), Duration(4, 10)]
        >>> notes = scoretools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ..  doctest::

        >>> print(format(voice))
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            \tweak edge-height #'(0.7 . 0)
            \times 4/5 {
                c'32
            }
        }

    Set `prolation` when making notes in a measure with a non-power-of-two denominator.

    Returns list of components.
    '''
    from abjad.tools import scoretools

    written_duration = durationtools.Duration(written_duration)
    total_duration = durationtools.Duration(total_duration)
    prolation = durationtools.Duration(prolation)
    prolation = fractions.Fraction(prolation)

    duration = prolation * written_duration
    current_duration = durationtools.Duration(0)
    result = []
    while current_duration + duration <= total_duration:
        result.append(scoretools.Note(pitch, written_duration))
        current_duration += duration
    remainder_duration = total_duration - current_duration
    if durationtools.Duration(0) < remainder_duration:
        multiplied_remainder = remainder_duration / prolation
        result.extend(scoretools.make_notes(pitch, [multiplied_remainder]))

    result = selectiontools.Selection(result)
    return result
