from abjad.tools.notetools.Note import Note
from abjad.tools import durationtools
from abjad.tools import sequencetools
import fractions


def make_quarter_notes_with_lilypond_multipliers(pitches, multiplied_durations):
    r'''.. versionadded:: 2.0

    Make quarter notes with `pitches` and `multiplied_durations`::

        abjad> notetools.make_quarter_notes_with_lilypond_multipliers([0, 2, 4, 5], [(1, 4), (1, 5), (1, 6), (1, 7)])
        [Note("c'4 * 1"), Note("d'4 * 4/5"), Note("e'4 * 2/3"), Note("f'4 * 4/7")]

    Read `pitches` cyclically where the length of `pitches` is
    less than the length of `multiplied_durations`::

        abjad> notetools.make_quarter_notes_with_lilypond_multipliers([0], [(1, 4), (1, 5), (1, 6), (1, 7)])
        [Note("c'4 * 1"), Note("c'4 * 4/5"), Note("c'4 * 2/3"), Note("c'4 * 4/7")]

    Read `multiplied_durations` cyclically where the length of
    `multiplied_durations` is less than the length of `pitches`::

        abjad> notetools.make_quarter_notes_with_lilypond_multipliers([0, 2, 4, 5], [(1, 5)])
        [Note("c'4 * 4/5"), Note("d'4 * 4/5"), Note("e'4 * 4/5"), Note("f'4 * 4/5")]

    Return list of zero or more newly constructed notes.

    .. versionchanged:: 2.0
        renamed ``construct.quarter_notes_with_multipliers()`` to
        ``notetools.make_quarter_notes_with_lilypond_multipliers()``.
    '''

    quarter_notes = []

    for pitch, duration in sequencetools.zip_sequences_cyclically(pitches, multiplied_durations):
        quarter_note = Note(pitch, durationtools.Duration(1, 4))
        duration_token = durationtools.duration_token_to_duration_pair(duration)
        duration = durationtools.Duration(*duration_token)
        multiplier = fractions.Fraction(duration / durationtools.Duration(1, 4))
        quarter_note.duration_multiplier = multiplier
        quarter_notes.append(quarter_note)

    return quarter_notes
