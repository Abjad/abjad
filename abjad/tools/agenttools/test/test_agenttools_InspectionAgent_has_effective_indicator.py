# -*- coding: utf-8 -*-
import abjad


def test_agenttools_InspectionAgent_has_effective_indicator_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.attach('foo', staff[2], scope=abjad.Staff)

    assert not abjad.inspect(staff).has_effective_indicator(str)
    assert not abjad.inspect(staff[0]).has_effective_indicator(str)
    assert not abjad.inspect(staff[1]).has_effective_indicator(str)
    assert abjad.inspect(staff[2]).has_effective_indicator(str)
    assert abjad.inspect(staff[3]).has_effective_indicator(str)
