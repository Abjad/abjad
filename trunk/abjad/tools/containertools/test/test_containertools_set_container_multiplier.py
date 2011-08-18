from abjad import *
import py.test


def test_containertools_set_container_multiplier_01():
    '''Set multiplier on fixed-duration tuplet
        by adjusting target duration.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert t.target_duration == Duration(2, 8)
    assert t.multiplier == Duration(2, 3)

    containertools.set_container_multiplier(t, Duration(5, 8))
    assert t.target_duration == Duration(15, 64)
    assert t.multiplier == Duration(5, 8)


def test_containertools_set_container_multiplier_02():
    '''Set multiplier on rigid measure by adjusting meter.'''

    t = Measure((3, 8), "c'8 d'8 e'8")
    assert contexttools.get_effective_time_signature(t).duration == Duration(3, 8)

    containertools.set_container_multiplier(t, Duration(2, 3))
    assert contexttools.get_effective_time_signature(t).duration == Duration(2, 8)
    assert py.test.raises(OverfullMeasureError, 't.format')
