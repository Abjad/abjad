# -*- encoding: utf-8 -*-
from abjad import *


def test_agenttools_InspectionAgent_has_indicator_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('foo', staff)

    assert inspect(staff).has_indicator(str)
    assert not inspect(staff[0]).has_indicator(str)
    assert not inspect(staff[1]).has_indicator(str)
    assert not inspect(staff[2]).has_indicator(str)
    assert not inspect(staff[3]).has_indicator(str)
