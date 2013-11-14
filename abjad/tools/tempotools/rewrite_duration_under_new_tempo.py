# -*- encoding: utf-8 -*-


def rewrite_duration_under_new_tempo(duration, tempo_1, tempo_2):
    r'''Rewrite prolated `duration` under new tempo.

    Given prolated `duration` governed by `tempo_1`,
    return new duration governed by `tempo_2`.

    Ensure that `duration` and new duration
    consume exactly the same amount of time in seconds.

    ..  container:: example

        **Example.** Consider the two tempo indications below. 
        
        ::

            >>> tempo_1 = marktools.Tempo(Duration(1, 4), 60)
            >>> tempo_2 = marktools.Tempo(Duration(1, 4), 90)

        The first tempo indication specifies quarter equal to ``60 MM``.

        The second tempo indication specifies quarter equal to ``90 MM``.

        The second tempo is ``3/2`` times as fast as the first:

        ::

            >>> tempo_2 / tempo_1
            Multiplier(3, 2)

        Note that a triplet eighth note `tempo_1` equals a regular eighth note
        under `tempo_2`:

        ::

            >>> tempotools.rewrite_duration_under_new_tempo(
            ...     Duration(1, 12), tempo_1, tempo_2)
            Duration(1, 8)

        And note that a regular eighth note under `tempo_1` equals a dotted
        sixteenth under `tempo_2`:

        ::

            >>> tempotools.rewrite_duration_under_new_tempo(
            ...     Duration(1, 8), tempo_1, tempo_2)
            Duration(3, 16)

    Returns duration.
    '''

    tempo_ratio = tempo_2 / tempo_1
    new_duration = tempo_ratio * duration

    return new_duration
