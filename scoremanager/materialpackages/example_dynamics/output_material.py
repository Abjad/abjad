# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from experimental.tools import handlertools


example_dynamics = handlertools.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_duration=durationtools.Duration(
		1,
		16
		)
	)
