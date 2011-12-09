from abjad import *


def test_Performer_most_likely_instrument_based_on_performer_name_01():

    flutist = scoretools.Performer(name='flutist')
    assert flutist.most_likely_instrument_based_on_performer_name == instrumenttools.Flute
