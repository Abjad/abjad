# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentationSpecifier_01():

    flutist = instrumenttools.Performer('Flute')
    flutist.instruments.append(instrumenttools.Flute())
    flutist.instruments.append(instrumenttools.AltoFlute())

    guitarist = instrumenttools.Performer('Guitar')
    guitarist.instruments.append(instrumenttools.Guitar())

    instrumentation_specifier = instrumenttools.InstrumentationSpecifier([flutist, guitarist])

    assert instrumentation_specifier.performer_count == 2
    assert instrumentation_specifier.instrument_count == 3
    assert instrumentation_specifier.performers == [flutist, guitarist]
