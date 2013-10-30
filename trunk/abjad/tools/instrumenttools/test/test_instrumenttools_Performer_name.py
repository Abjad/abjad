# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_name_01():

    performer = instrumenttools.Performer('Flutist')
    assert performer.name == 'Flutist'

    performer.name = 'Violinist'
    assert performer.name == 'Violinist'
