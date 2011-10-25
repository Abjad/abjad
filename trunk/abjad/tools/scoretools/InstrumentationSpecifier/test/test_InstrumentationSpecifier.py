from abjad import *


def test_InstrumentationSpecifier_01():

    flutist = scoretools.Performer('Flute')
    flutist.instruments.append(instrumenttools.Flute())
    flutist.instruments.append(instrumenttools.AltoFlute())

    guitarist = scoretools.Performer('Guitar')
    guitarist.instruments.append(instrumenttools.Guitar())

    instrumentation_specifier = scoretools.InstrumentationSpecifier([flutist, guitarist])

    assert instrumentation_specifier.performer_count == 2
    assert instrumentation_specifier.instrument_count == 3
    assert instrumentation_specifier.performers == [flutist, guitarist]
