from abjad.tools import durationtools
from abjad.tools import pitchtools
import handlertools


red_marcati = handlertools.ReiteratedArticulationHandler(
	articulation_list=['^', '.'],
	minimum_duration=durationtools.Duration(
		1,
		64
		),
	maximum_duration=durationtools.Duration(
		1,
		4
		),
	minimum_written_pitch=pitchtools.NamedChromaticPitch(
		'a,,,'
		),
	maximum_written_pitch=pitchtools.NamedChromaticPitch(
		"c''''"
		)
	)