from abjad import *


def test_instrumenttools_Accordion_is_transposing_01():

    accordion = instrumenttools.Accordion()

    assert not accordion.is_transposing
