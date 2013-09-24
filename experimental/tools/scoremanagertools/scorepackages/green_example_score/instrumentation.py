# -*- encoding: utf-8 -*-
from abjad import *


instrumentation=scoretools.InstrumentationSpecifier(
	performers=scoretools.PerformerInventory([
		scoretools.Performer(
			name='flutist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.AltoFlute()
				])
			),
		scoretools.Performer(
			name='guitarist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.Guitar()
				])
			)
		])
	)