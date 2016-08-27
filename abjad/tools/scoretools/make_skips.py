# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import selectiontools
from abjad.tools.topleveltools import attach


def make_skips(
    written_duration,
    multiplied_durations,
    ):
    '''Make `written_duration` skips with `multiplied_durations`:

    ::

        >>> scoretools.make_skips(
        ...     Duration(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)])
        Selection([Skip('s4 * 2'), Skip('s4 * 4/3'), Skip('s4 * 1'), Skip('s4 * 4/5')])

    Useful for making invisible layout voices.

    Returns selection.
    '''
    from abjad.tools import scoretools

    # initialize skips and written duration
    skips = []
    written_duration = durationtools.Duration(written_duration)

    # make skips
    for multiplied_duration in multiplied_durations:
        multiplied_duration = durationtools.Duration(multiplied_duration)
        skip = scoretools.Skip(written_duration)
        multiplier = multiplied_duration / written_duration
        attach(multiplier, skip)
        skips.append(skip)

    # return skips
    skips = selectiontools.Selection(skips)
    return skips
