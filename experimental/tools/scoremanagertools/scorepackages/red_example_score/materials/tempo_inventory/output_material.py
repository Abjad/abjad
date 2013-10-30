# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import durationtools


tempo_inventory = marktools.TempoMarkInventory([
	marktools.TempoMark(
		durationtools.Duration(1, 8),
		72
		),
	marktools.TempoMark(
		durationtools.Duration(1, 8),
		108
		),
	marktools.TempoMark(
		durationtools.Duration(1, 8),
		90
		),
	marktools.TempoMark(
		durationtools.Duration(1, 8),
		135
		)
	])
