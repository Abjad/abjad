# -*- encoding: utf-8 -*-


def rewrite_duration_under_new_tempo(duration, tempo_mark_1, tempo_mark_2):
    r'''Rewrite prolated `duration` under new tempo.

    Given prolated `duration` governed by `tempo_mark_1`,
    return new duration governed by `tempo_mark_2`.

    Ensure that `duration` and new duration
    consume exactly the same amount of time in seconds.

    ..  container:: example

        **Example.** Consider the two tempo indications below. 
        
        ::

            >>> tempo_mark_1 = contexttools.TempoMark(Duration(1, 4), 60)
            >>> tempo_mark_2 = contexttools.TempoMark(Duration(1, 4), 90)

        The first tempo indication specifies quarter equal to ``60 MM``.

        The second tempo indication specifies quarter equal to ``90 MM``.

        The second tempo is ``3/2`` times as fast as the first:

        ::

            >>> tempo_mark_2 / tempo_mark_1
            Multiplier(3, 2)

        Note that a triplet eighth note `tempo_mark_1` equals a regular eighth note
        under `tempo_mark_2`:

        ::

            >>> tempotools.rewrite_duration_under_new_tempo(
            ...     Duration(1, 12), tempo_mark_1, tempo_mark_2)
            Duration(1, 8)

        And note that a regular eighth note under `tempo_mark_1` equals a dotted
        sixteenth under `tempo_mark_2`:

        ::

            >>> tempotools.rewrite_duration_under_new_tempo(
            ...     Duration(1, 8), tempo_mark_1, tempo_mark_2)
            Duration(3, 16)

    Returns duration.
    '''

    tempo_ratio = tempo_mark_2 / tempo_mark_1
    new_duration = tempo_ratio * duration

    return new_duration
