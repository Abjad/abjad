# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_most_likely_instrument_based_on_performer_name_01():

    flutist = instrumenttools.Performer(name='flutist')
    assert flutist.most_likely_instrument_based_on_performer_name == instrumenttools.Flute


def test_instrumenttools_Performer_most_likely_instrument_based_on_performer_name_02():

    assert instrumenttools.Performer().most_likely_instrument_based_on_performer_name is None
    assert instrumenttools.Performer(name='foo').most_likely_instrument_based_on_performer_name is None
