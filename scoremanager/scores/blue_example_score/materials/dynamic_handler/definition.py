# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import handlertools


dynamic_handler = handlertools.ReiteratedDynamicHandler(
	dynamic_name='f',
	minimum_duration=durationtools.Duration(
		1,
		16
		)
	)