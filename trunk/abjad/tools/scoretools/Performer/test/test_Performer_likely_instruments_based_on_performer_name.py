from abjad import *


def test_Performer_likely_instruments_based_on_performer_name_01():

    flutist = scoretools.Performer(name='flutist')

    assert flutist.likely_instruments_based_on_performer_name == [
        instrumenttools.AltoFlute,
        instrumenttools.BassFlute,
        instrumenttools.ContrabassFlute,
        instrumenttools.Flute,
        instrumenttools.Piccolo]
