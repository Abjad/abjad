# -*- encoding: utf-8 -*-
from abjad import *
import blue_example_score


sargasso_measures = blue_example_score.makers.SargassoMeasureMaker(
    measures_are_scaled=False,
    measures_are_split=False,
    measures_are_shuffled=False,
    )