from abjad import *


def test_SchemeNumber___int____01():

    a = schemetools.SchemeNumber(3.5)

    assert int(a) == 3
