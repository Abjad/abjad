# -*- coding: utf-8 -*-
from abjad import *


def test_schemetools_SchemeAssociativeList___init___01():

    scheme_associative_list = schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
    assert format(scheme_associative_list) == "#'((space . 2) (padding . 0.5))"
