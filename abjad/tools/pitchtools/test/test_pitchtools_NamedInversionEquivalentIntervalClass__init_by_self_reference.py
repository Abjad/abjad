# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_self_reference_01():

    dic_1 = pitchtools.NamedInversionEquivalentIntervalClass('major', 2)
    dic_2 = pitchtools.NamedInversionEquivalentIntervalClass(dic_1)

    assert str(dic_1) == '+M2'
    assert str(dic_2) == '+M2'
