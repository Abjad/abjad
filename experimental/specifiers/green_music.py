from abjad import *
from abjad.tools import contexttools
from abjad.tools import durationtools
from experimental.tools.scftools import specifiers


music_specifier = specifiers.MusicSpecifier([
	specifiers.MusicContributionSpecifier(
		[specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())],
		name='green violin pizzicati',
		description='upper register violin pizzicati'
		)
	],
	name='green music'
	)
