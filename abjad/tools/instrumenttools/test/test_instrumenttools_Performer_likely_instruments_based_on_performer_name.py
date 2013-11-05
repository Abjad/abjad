# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_likely_instruments_based_on_performer_name_01():

    flutist = instrumenttools.Performer(name='flutist')

    assert flutist.likely_instruments_based_on_performer_name == [
        instrumenttools.AltoFlute,
        instrumenttools.BassFlute,
        instrumenttools.ContrabassFlute,
        instrumenttools.Flute,
        instrumenttools.Piccolo]


def test_instrumenttools_Performer_likely_instruments_based_on_performer_name_02():

    assert instrumenttools.Performer().likely_instruments_based_on_performer_name == []
    assert instrumenttools.Performer(name='foo').likely_instruments_based_on_performer_name == []
