# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_indicator_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('color', staff)

    assert inspect(staff).get_indicator('color') == 'color'
    assert pytest.raises(Exception, "inspect(staff[0]).get_indicator('color')")
    assert pytest.raises(Exception, "inspect(staff[1]).get_indicator('color')")
    assert pytest.raises(Exception, "inspect(staff[2]).get_indicator('color')")
    assert pytest.raises(Exception, "inspect(staff[3]).get_indicator('color')")


def test_agenttools_InspectionAgent_get_indicator_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    attach('color', staff)

    assert inspect(staff).get_indicator(str) == 'color'
    assert pytest.raises(Exception, "inspect(staff[0]).get_indicator(str)")
    assert pytest.raises(Exception, "inspect(staff[1]).get_indicator(str)")
    assert pytest.raises(Exception, "inspect(staff[2]).get_indicator(str)")
    assert pytest.raises(Exception, "inspect(staff[3]).get_indicator(str)")
