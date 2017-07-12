# -*- coding: utf-8 -*-
import abjad


def test_schemetools_SchemeAssociativeList___init___01():

    scheme_associative_list = abjad.SchemeAssociativeList(('space', 2), ('padding', 0.5))
    assert format(scheme_associative_list) == "#'((space . 2) (padding . 0.5))"
