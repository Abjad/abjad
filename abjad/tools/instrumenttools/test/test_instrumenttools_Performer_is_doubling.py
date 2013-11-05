# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_is_doubling_01():

    performer = instrumenttools.Performer('Flutist')
    performer.instruments.append(instrumenttools.Flute())
    assert not performer.is_doubling

    performer.instruments.append(instrumenttools.Piccolo())
    assert performer.is_doubling
