# -*- coding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_has_effective_indicator_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('foo', staff[2], scope=Staff)

    assert not inspect_(staff).has_effective_indicator(str)
    assert not inspect_(staff[0]).has_effective_indicator(str)
    assert not inspect_(staff[1]).has_effective_indicator(str)
    assert inspect_(staff[2]).has_effective_indicator(str)
    assert inspect_(staff[3]).has_effective_indicator(str)
