# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools


def durate_pitch_contour_reservoir(pitch_contour_reservoir):
    r'''Durates pitch contour reservoir.
    '''

    instrument_names = [
        'First Violin',
        'Second Violin',
        'Viola',
        'Cello',
        'Bass',
        ]

    durated_reservoir = {}

    for i, instrument_name in enumerate(instrument_names):
        long_duration = durationtools.Duration(1, 2) * pow(2, i)
        short_duration = long_duration / 2
        rest_duration = long_duration * durationtools.Multiplier(3, 2)

        div = rest_duration // durationtools.Duration(3, 2)
        mod = rest_duration % durationtools.Duration(3, 2)

        initial_rest = scoretools.MultimeasureRest((3, 2)) * div
        if mod:
            initial_rest += scoretools.make_rests(mod)

        durated_contours = [tuple(initial_rest)]

        pitch_contours = pitch_contour_reservoir[instrument_name]
        durations = [long_duration, short_duration]
        counter = 0
        for pitch_contour in pitch_contours:
            contour = []
            for pitch in pitch_contour:
                contour.extend(
                    scoretools.make_leaves([pitch], [durations[counter]])
                    )
                counter = (counter + 1) % 2
            durated_contours.append(tuple(contour))

        durated_reservoir[instrument_name] = tuple(durated_contours)

    return durated_reservoir