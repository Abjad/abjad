# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools


tempo_inventory = indicatortools.TempoInventory([
	indicatortools.Tempo(
		durationtools.Duration(1, 8),
		72
		),
	indicatortools.Tempo(
		durationtools.Duration(1, 8),
		108
		),
	indicatortools.Tempo(
		durationtools.Duration(1, 8),
		90
		),
	indicatortools.Tempo(
		durationtools.Duration(1, 8),
		135
		)
	])
