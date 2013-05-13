from abjad.tools import contexttools
from abjad.tools import durationtools


tempo_inventory = contexttools.TempoMarkInventory([
	contexttools.TempoMark(
		durationtools.Duration(1, 8),
		72
		),
	contexttools.TempoMark(
		durationtools.Duration(1, 8),
		108
		),
	contexttools.TempoMark(
		durationtools.Duration(1, 8),
		90
		),
	contexttools.TempoMark(
		durationtools.Duration(1, 8),
		135
		)
	])