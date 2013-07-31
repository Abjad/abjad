# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_containertools_set_container_multiplier_01():
    r'''Set multiplier on fixed-duration tuplet
    by adjusting target duration.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert t.target_duration == Duration(2, 8)
    assert t.multiplier == Duration(2, 3)

    containertools.set_container_multiplier(t, Duration(5, 8))
    assert t.target_duration == Duration(15, 64)
    assert t.multiplier == Duration(5, 8)


def test_containertools_set_container_multiplier_02():
    r'''Set multiplier on rigid measure by adjusting time signature.
    '''

    t = Measure((3, 8), "c'8 d'8 e'8")
    assert t.get_effective_context_mark(
        contexttools.TimeSignatureMark).duration == Duration(3, 8)

    containertools.set_container_multiplier(t, Duration(2, 3))
    assert t.get_effective_context_mark(
        contexttools.TimeSignatureMark).duration == Duration(2, 8)
    assert py.test.raises(OverfullContainerError, 't.lilypond_format')
