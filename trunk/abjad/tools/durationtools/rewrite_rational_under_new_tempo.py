def rewrite_rational_under_new_tempo(prolated_duration_1, tempo_mark_1, tempo_mark_2):
    r'''.. versionadded:: 2.0

    Given `prolated_duration_1` governed by `tempo_mark_1`,
    return `prolated_duration_2` governed by `tempo_mark_2`
    such that `prolated_duration_1` and `prolated_duration_2`
    consume exactly the same amount of time in seconds.

    Consider the two tempo indications below. ::

        abjad> from abjad.tools import durationtools

    ::

        abjad> tempo_mark_1 = contexttools.TempoMark(Duration(1, 4), 60)
        abjad> tempo_mark_2 = contexttools.TempoMark(Duration(1, 4), 90)

    The first tempo indication specifies quarter = 60 MM.
    The second tempo indication specifies quarter = 90 MM.

    The second tempo is 1 1/2 times as fast as the first. ::

        abjad> tempo_mark_2 / tempo_mark_1
        Duration(3, 2)

    An triplet eighth note at tempo 1 equals a regular eighth note
    at tempo 2. ::

        abjad> durationtools.rewrite_rational_under_new_tempo(Duration(1, 12), tempo_mark_1, tempo_mark_2)
        Duration(1, 8)

    Conversely, a regular eighth not at tempo 1 equals a dotted
    sixteenth at tempo 2. ::

        abjad> durationtools.rewrite_rational_under_new_tempo(Duration(1, 8), tempo_mark_1, tempo_mark_2)
        Duration(3, 16)

    Return fraction.
    '''

    tempo_ratio = tempo_mark_2 / tempo_mark_1
    prolated_duration_2 = tempo_ratio * prolated_duration_1

    return prolated_duration_2
