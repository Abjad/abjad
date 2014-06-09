# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.scores.red_example_score.makers import SargassoMeasureMaker


example_sargasso_measures = SargassoMeasureMaker(
    measure_denominator=4,
    measure_numerator_talea=(2, 2, 2, 2, 1, 1, 4, 4),
    measure_division_denominator=16,
    measure_division_talea=(1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4),
    total_duration=durationtools.Duration(11, 2),
    measures_are_scaled=True,
    measures_are_split=True,
    measures_are_shuffled=True,
    )