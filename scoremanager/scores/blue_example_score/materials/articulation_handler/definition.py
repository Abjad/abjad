# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import handlertools


articulation_handler = handlertools.ReiteratedArticulationHandler(
    articulation_list=['^', '.'],
    minimum_duration=durationtools.Duration(1, 64),
    maximum_duration=durationtools.Duration(1, 4),
    minimum_written_pitch=pitchtools.NamedPitch('a,,,'),
    maximum_written_pitch=pitchtools.NamedPitch("c''''"),
    )