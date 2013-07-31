# -*- encoding: utf-8 -*-
from abjad import *


def test_SchemeAssociativeList___init___01():

    scheme_associative_list = schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
    assert scheme_associative_list.lilypond_format == "#'((space . 2) (padding . 0.5))"
