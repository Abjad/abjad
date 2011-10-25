from abjad import *


def test_Performer_designation_01():

    performer = scoretools.Performer('Flutist')
    assert performer.designation == 'Flutist'

    performer.designation = 'Violinist'
    assert performer.designation == 'Violinist'
