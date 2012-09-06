import fractions
from abjad.tools import durationtools
from abjad.tools import mathtools


def make_accelerating_notes_with_lilypond_multipliers(pitches, total, start, stop, exp='cosine', written='8'):
    '''Make accelerating notes with LilyPond multipliers::

        >>> pitches = [1, 2]
        >>> total = (1, 2)
        >>> start = (1, 4)
        >>> stop = (1, 8)
        >>> args = [pitches, total, start, stop]

    ::

        >>> notes = notetools.make_accelerating_notes_with_lilypond_multipliers(*args)

    ::

        >>> notes
        [Note("cs'8 * 113/64"), Note("d'8 * 169/128"), Note("cs'8 * 117/128")]

    ::

        >>> Voice(notes).prolated_duration
        Duration(1, 2)

    Set note pitches cyclically from `pitches`.

    Return as many interpolation values as necessary to fill the `total` duration requested.

    Interpolate durations from `start` to `stop`.

    Set note durations to `written` duration times computed interpolated multipliers.

    Return list of notes.

    .. versionchanged:: 2.0
        renamed ``construct.notes_curve()`` to
        ``notetools.make_accelerating_notes_with_lilypond_multipliers()``.
    '''
    from abjad.tools import notetools

    # initialize input arguments as durations
    total = durationtools.Duration(total)
    start = durationtools.Duration(start)
    stop = durationtools.Duration(stop)
    written = durationtools.Duration(written)

    # change mathtools input arguments to vanilla rationals
    args = [fractions.Fraction(x) for x in (total, start, stop)]
    args.append(exp)

    # calculate lilypond multipliers
    multipliers = mathtools.interpolate_divide(*args)

    # change floats to rationals
    multipliers = [fractions.Fraction(int(round(x * 2**10)), 2**10) for x in multipliers]

    # make notes
    result = []
    for i, multiplier in enumerate(multipliers):
        note = notetools.Note(pitches[i % len(pitches)], written)
        note.duration_multiplier = fractions.Fraction(multiplier / written)
        result.append(note)

    # return result
    return result
