# -*- encoding: utf-8 -*-
from abjad import *


instrumentation=instrumenttools.InstrumentationSpecifier(
	performers=instrumenttools.PerformerInventory([
		instrumenttools.Performer(
			name='flutist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.AltoFlute()
				])
			),
		instrumenttools.Performer(
			name='guitarist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.Guitar()
				])
			)
		])
	)