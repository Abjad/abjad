# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import sequencetools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import attach


def make_multiplied_quarter_notes(
    pitches,
    multiplied_durations,
    ):
    r'''Make quarter notes with `pitches` and `multiplied_durations`:

    ::

        >>> args = [[0, 2, 4, 5], [(1, 4), (1, 5), (1, 6), (1, 7)]]
        >>> scoretools.make_multiplied_quarter_notes(*args)
        Selection([Note("c'4 * 1"), Note("d'4 * 4/5"), Note("e'4 * 2/3"), Note("f'4 * 4/7")])

    Read `pitches` cyclically where the length of `pitches` is
    less than the length of `multiplied_durations`:

    ::

        >>> args = [[0], [(1, 4), (1, 5), (1, 6), (1, 7)]]
        >>> scoretools.make_multiplied_quarter_notes(*args)
        Selection([Note("c'4 * 1"), Note("c'4 * 4/5"), Note("c'4 * 2/3"), Note("c'4 * 4/7")])

    Read `multiplied_durations` cyclically where the length of
    `multiplied_durations` is less than the length of `pitches`:

    ::

        >>> args = [[0, 2, 4, 5], [(1, 5)]]
        >>> scoretools.make_multiplied_quarter_notes(*args)
        Selection([Note("c'4 * 4/5"), Note("d'4 * 4/5"), Note("e'4 * 4/5"), Note("f'4 * 4/5")])

    Returns list of zero or more newly constructed notes.
    '''
    from abjad.tools import scoretools

    multiplied_durations = [
        durationtools.Duration(x) for x in multiplied_durations]
    quarter_notes = []

    sequences = [pitches, multiplied_durations]
    for pitch, duration in sequencetools.zip_sequences(sequences, cyclic=True):
        quarter_note = scoretools.Note(pitch, durationtools.Duration(1, 4))
        duration = durationtools.Duration(duration)
        multiplier = durationtools.Multiplier(
            duration / durationtools.Duration(1, 4))
        attach(multiplier, quarter_note)
        quarter_notes.append(quarter_note)

    quarter_notes = selectiontools.Selection(quarter_notes)
    return quarter_notes
