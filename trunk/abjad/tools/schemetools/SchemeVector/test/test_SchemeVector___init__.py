from abjad import *


def test_SchemeVector___init___01():

    vector = schemetools.SchemeVector(1, 2, 3, 4)
    assert str(vector) == '(1 2 3 4)'
    assert vector.format == "#'(1 2 3 4)"


def test_SchemeVector___init___02():

    vector = schemetools.SchemeVector(True, False, 1, 0)
    assert str(vector) == "(#t #f 1 0)"
    assert vector.format == "#'(#t #f 1 0)"
