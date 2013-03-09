from abjad import *
import py.test


def test_Measure_empty_01():
    assert py.test.raises(Exception, '''t = Measure(None, "c'8 d'8 e'8 f'8")''')


def test_Measure_empty_02():
    t = Measure((4, 4), [])
    assert repr(t) == 'Measure(4/4)'
    assert str(t) == '|4/4|'
    assert py.test.raises(UnderfullContainerError, 't.lilypond_format')
    assert len(t) == 0
    assert t.preprolated_duration == 0
    assert t.duration == 0
    assert not wellformednesstools.is_well_formed_component(t)


def test_Measure_empty_03():
    t = Measure((4, 5), [])
    assert repr(t) == 'Measure(4/5)'
    assert str(t) == '|4/5|'
    assert py.test.raises(UnderfullContainerError, 't.lilypond_format')
    assert len(t) == 0
    assert t.preprolated_duration == 0
    assert t.duration == 0
    assert not wellformednesstools.is_well_formed_component(t)
