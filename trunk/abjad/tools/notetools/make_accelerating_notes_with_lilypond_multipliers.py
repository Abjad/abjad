from abjad.tools.notetools.Note import Note
from abjad.tools import durationtools
from abjad.tools import mathtools
import fractions


def make_accelerating_notes_with_lilypond_multipliers(pitches, total, start, stop, exp='cosine',
    written = durationtools.Duration(1, 8)):
    '''Make accelerating notes with LilyPond multipliers::

        abjad> notetools.make_accelerating_notes_with_lilypond_multipliers([1,2], (1, 2), (1, 4), (1, 8))
        [Note("cs'8 * 113/64"), Note("d'8 * 169/128"), Note("cs'8 * 117/128")]

    ::

        abjad> voice = Voice(_)
        abjad> voice.prolated_duration
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

    total = fractions.Fraction(*durationtools.duration_token_to_duration_pair(total))
    start = fractions.Fraction(*durationtools.duration_token_to_duration_pair(start))
    stop = fractions.Fraction(*durationtools.duration_token_to_duration_pair(stop))
    written = durationtools.Duration(*durationtools.duration_token_to_duration_pair(written))

    dts = mathtools.interpolate_divide(total, start, stop, exp)

    # change floats to rationals
    dts = [fractions.Fraction(int(round(x * 2**10)), 2**10) for x in dts]

    # make notes
    result = []
    for i, dt in enumerate(dts):
        note = Note(pitches[i % len(pitches)], written)
        note.duration_multiplier = fractions.Fraction(dt / written)
        result.append(note)
    return result
