from abjad import *


def test_Performer_make_performer_name_instrument_dictionary_01():

    performer = scoretools.Performer()
    dictionary = performer.make_performer_name_instrument_dictionary()

    assert 'pianist' in dictionary
    assert 'guitarist' in dictionary
    assert 'violinist' in dictionary

    assert dictionary['bassoonist'] == [instrumenttools.Bassoon, instrumenttools.Contrabassoon]
