from abjad import *
from abjad.tools import instrumenttools


def test_HumanMusician_musician_name_01():

    human_musician = instrumenttools.HumanMusician('Flutist')
    assert human_musician.musician_name == 'Flutist'

    human_musician.musician_name = 'Violinist'
    assert human_musician.musician_name == 'Violinist'
