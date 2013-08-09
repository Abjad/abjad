# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_containertools_set_container_multiplier_01():
    r'''Set multiplier on fixed-duration tuplet
    by adjusting target duration.
    '''

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert tuplet.target_duration == Duration(2, 8)
    assert tuplet.multiplier == Duration(2, 3)

    containertools.set_container_multiplier(tuplet, Duration(5, 8))
    assert tuplet.target_duration == Duration(15, 64)
    assert tuplet.multiplier == Duration(5, 8)


def test_containertools_set_container_multiplier_02():
    r'''Set multiplier on measure by adjusting time signature.
    '''

    measure = Measure((3, 8), "c'8 d'8 e'8")
    assert measure.time_signature.duration == Duration(3, 8)

    containertools.set_container_multiplier(measure, Duration(2, 3))
    assert measure.time_signature.duration == Duration(2, 8)
    assert py.test.raises(OverfullContainerError, 'measure.lilypond_format')
