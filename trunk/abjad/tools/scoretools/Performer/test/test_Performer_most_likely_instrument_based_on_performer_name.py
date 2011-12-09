from abjad import *


def test_Performer_most_likely_instrument_based_on_performer_name_01():

    flutist = scoretools.Performer(name='flutist')
    assert flutist.most_likely_instrument_based_on_performer_name == instrumenttools.Flute


def test_Performer_most_likely_instrument_based_on_performer_name_02():

    assert scoretools.Performer().most_likely_instrument_based_on_performer_name is None
    assert scoretools.Performer(name='foo').most_likely_instrument_based_on_performer_name is None
