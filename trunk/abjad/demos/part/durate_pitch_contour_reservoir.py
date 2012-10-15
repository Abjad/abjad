from fractions import Fraction
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools import resttools


def durate_pitch_contour_reservoir(pitch_contour_reservoir):

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
        rest_duration = long_duration * Fraction(3, 2)
        initial_rest = resttools.make_rests(rest_duration)

        durated_contours = [tuple(initial_rest)]

        pitch_contours = pitch_contour_reservoir[instrument_name]
        durations = [long_duration, short_duration]
        counter = 0
        for pitch_contour in pitch_contours:
            contour = []
            for pitch in pitch_contour:
                contour.extend(leaftools.make_leaves([pitch], [durations[counter]]))
                counter = (counter + 1) % 2
            durated_contours.append(tuple(contour))

        durated_reservoir[instrument_name] = tuple(durated_contours)

    return durated_reservoir

