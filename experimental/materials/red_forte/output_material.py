from abjad.tools import durationtools
import handlertools


red_forte = handlertools.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_duration=durationtools.Duration(
		1,
		16
		)
	)
