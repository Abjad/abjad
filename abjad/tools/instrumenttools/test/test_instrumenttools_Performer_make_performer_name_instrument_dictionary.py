# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Performer_make_performer_name_instrument_dictionary_01():

    performer = instrumenttools.Performer()
    dictionary = performer.make_performer_name_instrument_dictionary()

    assert 'pianist' in dictionary
    assert 'guitarist' in dictionary
    assert 'violinist' in dictionary

    assert dictionary['bassoonist'] == [instrumenttools.Bassoon, instrumenttools.Contrabassoon]
