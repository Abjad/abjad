import abjad
import pytest


def test_scoretools_Measure_empty_01():

    measure = abjad.Measure((4, 4), [])

    assert str(measure) == 'Measure((4, 4))'
    assert pytest.raises(abjad.UnderfullContainerError, 'format(measure)')
    assert len(measure) == 0
    assert measure._get_preprolated_duration() == 0
    assert abjad.inspect(measure).get_duration() == 0
    assert not abjad.inspect(measure).is_well_formed()


def test_scoretools_Measure_empty_02():

    measure = abjad.Measure((4, 5), [])

    assert str(measure) == 'Measure((4, 5))'
    assert pytest.raises(abjad.UnderfullContainerError, 'format(measure)')
    assert len(measure) == 0
    assert measure._get_preprolated_duration() == 0
    assert abjad.inspect(measure).get_duration() == 0
    assert not abjad.inspect(measure).is_well_formed()
