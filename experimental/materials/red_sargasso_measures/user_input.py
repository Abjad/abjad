from abjad.tools.durationtools import Duration
from scftools.editors import UserInputWrapper


user_input_wrapper = UserInputWrapper([
	('measure_denominator', 4),
	('measure_numerator_talea', [2, 2, 2, 2, 1, 1, 4, 4]),
	('measure_division_denominator', 16),
	('measure_division_talea', [1, 1, 2, 3, 1, 2, 3, 4, 1, 1, 1, 1, 4]),
	('total_duration', Duration(11, 2)),
	('measures_are_scaled', True),
	('measures_are_split', True),
	('measures_are_shuffled', True)])