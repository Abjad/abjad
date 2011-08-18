from abjad import *
from abjad.tools import tonalitytools


def test_ScaleDegree_name_01():

    assert tonalitytools.ScaleDegree(1).name == 'tonic'
    assert tonalitytools.ScaleDegree(2).name == 'superdominant'
    assert tonalitytools.ScaleDegree(3).name == 'mediant'
    assert tonalitytools.ScaleDegree(4).name == 'subdominant'
    assert tonalitytools.ScaleDegree(5).name == 'dominant'
    assert tonalitytools.ScaleDegree(6).name == 'submediant'
    assert tonalitytools.ScaleDegree(7).name == 'leading tone'
