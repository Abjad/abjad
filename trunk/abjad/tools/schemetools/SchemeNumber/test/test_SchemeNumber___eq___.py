from abjad import *


def test_SchemeNumber___eq____01():

    a = schemetools.SchemeNumber(3)
    b = schemetools.SchemeNumber(4)

    assert a != b

def test_SchemeNumber___eq____02():

    a = schemetools.SchemeNumber(3)
    b = schemetools.SchemeNumber(3)

    assert a == b

def test_SchemeNumber___eq____03():

    a = schemetools.SchemeNumber(3)
    b = schemetools.SchemeNumber(3.0)

    assert a == b
