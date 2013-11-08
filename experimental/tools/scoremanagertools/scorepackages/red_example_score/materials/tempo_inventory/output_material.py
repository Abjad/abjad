# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools


tempo_inventory = marktools.TempoInventory([
	marktools.Tempo(
		durationtools.Duration(1, 8),
		72
		),
	marktools.Tempo(
		durationtools.Duration(1, 8),
		108
		),
	marktools.Tempo(
		durationtools.Duration(1, 8),
		90
		),
	marktools.Tempo(
		durationtools.Duration(1, 8),
		135
		)
	])
