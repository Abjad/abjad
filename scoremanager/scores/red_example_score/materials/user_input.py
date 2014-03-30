# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager import iotools


user_input_wrapper = iotools.UserInputWrapper([
	('measure_denominator', None),
	('measure_numerator_talea', None),
	('measure_division_denominator', None),
	('measure_division_talea', None),
	('total_duration', None),
	('measures_are_scaled', None),
	('measures_are_split', None),
	('measures_are_shuffled', None)])