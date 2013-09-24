# -*- encoding: utf-8 -*-
from abjad import *


instrumentation=scoretools.InstrumentationSpecifier(
	performers=scoretools.PerformerInventory([
		scoretools.Performer(
			name='hornist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.FrenchHorn()
				])
			),
		scoretools.Performer(
			name='trombonist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.TenorTrombone()
				])
			),
		scoretools.Performer(
			name='violinist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.Violin()
				])
			),
		scoretools.Performer(
			name='cellist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.Cello()
				])
			),
		scoretools.Performer(
			name='pianist',
			instruments=instrumenttools.InstrumentInventory([
				instrumenttools.Piano()
				])
			),
		scoretools.Performer(
			name='percussionist',
			instruments=instrumenttools.InstrumentInventory([])
			)
		])
	)