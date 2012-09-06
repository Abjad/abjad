import fractions
from abjad.tools import durationtools


def make_repeated_notes_with_shorter_notes_at_end(pitch, written_duration, total_duration, prolation=1):
    r'''Make repeated notes with `pitch` and `written_duration` summing to 
    `total_duration` under `prolation`::

        >>> args = [0, Duration(1, 16), Duration(1, 4)]
        >>> notes = notetools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ::

        >>> f(voice)
        \new Voice {
            c'16
            c'16
            c'16
            c'16
        }

    Fill binary remaining duration with binary notes of lesser written duration::

        >>> args = [0, Duration(1, 16), Duration(9, 32)]
        >>> notes = notetools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ::

        >>> f(voice)
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'32
        }

    Fill nonbinary remaining duration with ad hoc tuplet::

        >>> args = [0, Duration(1, 16), Duration(4, 10)]
        >>> notes = notetools.make_repeated_notes_with_shorter_notes_at_end(*args)
        >>> voice = Voice(notes)

    ::

        >>> f(voice)
        \new Voice {
            c'16
            c'16
            c'16
            c'16
            c'16
            c'16
            \times 4/5 {
                c'32
            }
        }

    Set `prolation` when constructing notes in a nonbinary measure.

    Return list of newly constructed components.

    .. versionchanged:: 2.0
        renamed ``construct.note_train()`` to
        ``notetools.make_repeated_notes_with_shorter_notes_at_end()``.
    '''
    from abjad.tools import notetools

    written_duration = durationtools.Duration(written_duration)
    total_duration = durationtools.Duration(total_duration)
    prolation = durationtools.Duration(prolation)
    prolation = fractions.Fraction(prolation)

    prolated_duration = prolation * written_duration
    current_duration = durationtools.Duration(0)
    result = []
    while current_duration + prolated_duration <= total_duration:
        result.append(notetools.Note(pitch, written_duration))
        current_duration += prolated_duration
    remainder_duration = total_duration - current_duration
    if durationtools.Duration(0) < remainder_duration:
        multiplied_remainder = remainder_duration / prolation
        result.extend(notetools.make_notes(pitch, [multiplied_remainder]))
    return result
