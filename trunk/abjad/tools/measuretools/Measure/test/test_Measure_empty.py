# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Measure_empty_01():
    assert py.test.raises(
        Exception, r'''t = Measure(None, "c'8 d'8 e'8 f'8")''')


def test_Measure_empty_02():
    measure = Measure((4, 4), [])
    assert repr(measure) == 'Measure(4/4)'
    assert str(measure) == '|4/4|'
    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')
    assert len(measure) == 0
    assert measure._preprolated_duration == 0
    assert inspect(measure).get_duration() == 0
    assert not select(measure).is_well_formed()


def test_Measure_empty_03():
    measure = Measure((4, 5), [])
    assert repr(measure) == 'Measure(4/5)'
    assert str(measure) == '|4/5|'
    assert py.test.raises(UnderfullContainerError, 'measure.lilypond_format')
    assert len(measure) == 0
    assert measure._preprolated_duration == 0
    assert inspect(measure).get_duration() == 0
    assert not select(measure).is_well_formed()
