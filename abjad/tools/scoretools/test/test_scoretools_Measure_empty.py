# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Measure_empty_01():

    measure = Measure((4, 4), [])

    assert str(measure) == 'Measure((4, 4))'
    assert pytest.raises(UnderfullContainerError, 'format(measure)')
    assert len(measure) == 0
    assert measure._preprolated_duration == 0
    assert inspect_(measure).get_duration() == 0
    assert not inspect_(measure).is_well_formed()


def test_scoretools_Measure_empty_02():

    measure = Measure((4, 5), [])

    assert str(measure) == 'Measure((4, 5))'
    assert pytest.raises(UnderfullContainerError, 'format(measure)')
    assert len(measure) == 0
    assert measure._preprolated_duration == 0
    assert inspect_(measure).get_duration() == 0
    assert not inspect_(measure).is_well_formed()
