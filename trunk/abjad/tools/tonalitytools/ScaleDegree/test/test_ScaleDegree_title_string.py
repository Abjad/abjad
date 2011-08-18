from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree_title_string_01():

    assert tonalitytools.ScaleDegree(1).title_string == 'One'
    assert tonalitytools.ScaleDegree(2).title_string == 'Two'
    assert tonalitytools.ScaleDegree(3).title_string == 'Three'
    assert tonalitytools.ScaleDegree(4).title_string == 'Four'
    assert tonalitytools.ScaleDegree(5).title_string == 'Five'
    assert tonalitytools.ScaleDegree(6).title_string == 'Six'
    assert tonalitytools.ScaleDegree(7).title_string == 'Seven'


def test_ScaleDegree_title_string_02():

    assert tonalitytools.ScaleDegree('sharp', 4).title_string == 'SharpFour'
    assert tonalitytools.ScaleDegree('flat', 6).title_string == 'FlatSix'
