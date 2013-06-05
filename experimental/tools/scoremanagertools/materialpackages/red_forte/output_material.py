from abjad.tools import durationtools
from experimental.tools import handlertools


red_forte = handlertools.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_duration=durationtools.Duration(
		1,
		16
		)
	)
