# -*- encoding: utf-8 -*-
from abjad import *


def test_Component_start_offset_01():
    voice = Voice(notetools.make_repeated_notes(16))
    for i, x in enumerate(voice):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_02():
    staff = Staff(notetools.make_repeated_notes(16))
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_03():
    staff = Staff(notetools.make_repeated_notes(16))
    staff[10] = Rest((1, 8))
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_04():
    staff = Staff(notetools.make_repeated_notes(16))
    staff[10:10] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_05():
    staff = Staff(notetools.make_repeated_notes(16))
    staff[10:12] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_06():
    r'''Offset works with voices.
    '''

    v1 = Voice(notetools.make_repeated_notes(16))
    v2 = Voice(notetools.make_repeated_notes(16))
    v1.name = v2.name = 'voice'
    container = Container([v1, v2])
    for i, x in enumerate(container.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_07():
    t = tuplettools.FixedDurationTuplet(Duration(1,4), notetools.make_repeated_notes(3))
    for i, x in enumerate(t):
        assert x.get_timespan().start_offset == i * Duration(1, 12)


def test_Component_start_offset_08():
    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    voice = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
    offset = 0
    for x, d in zip(voice.select_leaves(), [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]):
        assert x.get_timespan().start_offset == offset
        offset += Duration(*d)


def test_Component_start_offset_09():
    r'''Offset works on nested tuplets.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tp, Note("c'4")])
    offset = 0
    for x, d in zip(t.select_leaves(), [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]):
        assert x.get_timespan().start_offset == offset
        offset += Duration(*d)


def test_Component_start_offset_10():
    r'''Offset works with parallel structures.
    '''

    v1 = Voice(notetools.make_repeated_notes(16))
    v2 = Voice(notetools.make_repeated_notes(16))
    staff = Staff([v1, v2])
    staff.is_parallel = True
    for i, x in enumerate(v1):
        assert x.get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_11():
    r'''Offset on leaves works in nested contexts.
    '''

    v = Voice(notetools.make_repeated_notes(4))
    staff = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
    for i, x in enumerate(staff.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(v.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8) + Duration(1, 8)


def test_Component_start_offset_12():
    r'''Offset on leaves works in sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([v1, v2])
    for i, x in enumerate(v1.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_13():
    r'''Offset on leaves works in nested parallel contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([v1, v2])
    staff.is_parallel = True
    for i, x in enumerate(v1.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8)


def test_Component_start_offset_14():
    r'''Offset on leaves works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([Container([v1, v2]), v3])
    staff[0].is_parallel = True
    for i, x in enumerate(v3.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_15():
    r'''Offset on leaves works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([v3, Container([v1, v2])])
    staff[1].is_parallel = True
    for i, x in enumerate(v1.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8) + Duration(1, 2)
    for i, x in enumerate(v2.select_leaves()):
        assert x.get_timespan().start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_16():
    r'''Offsets works on sequential voices.
    '''

    staff = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    staff[0].name = staff[1].name = 'voice'
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(4, 8)


def test_Component_start_offset_17():
    r'''Prolated offset does NOT go across sequential staves.
    '''

    container = Container([Staff(notetools.make_repeated_notes(4)), Staff(notetools.make_repeated_notes(4))])
    container[0].name = container[1].name = 'staff'
    assert container[0].get_timespan().start_offset == Duration(0)
    assert container[1].get_timespan().start_offset == Duration(1, 2)


def test_Component_start_offset_18():
    r'''Offsets works with nested voices.
    '''

    staff = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    for i, x in enumerate(staff):
        assert x.get_timespan().start_offset == i * Duration(4, 8)


def test_Component_start_offset_19():
    r'''Offsets works on sequential tuplets.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3)) * 3)
    assert voice[0].get_timespan().start_offset == 0 * Duration(1, 4)
    assert voice[1].get_timespan().start_offset == 1 * Duration(1, 4)
    assert voice[2].get_timespan().start_offset == 2 * Duration(1, 4)


def test_Component_start_offset_20():
    r'''Offsets work on tuplets between notes.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    voice = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
    assert voice[0].get_timespan().start_offset == 0 * Duration(1, 8)
    assert voice[1].get_timespan().start_offset == 1 * Duration(1, 8)
    assert voice[2].get_timespan().start_offset == 3 * Duration(1, 8)


def test_Component_start_offset_21():
    r'''Offsets work on nested tuplets.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tp, Note("c'4")])
    assert t[0].get_timespan().start_offset == 0 * Duration(1, 6)
    assert t[1].get_timespan().start_offset == 1 * Duration(1, 6)
    assert t[2].get_timespan().start_offset == 2 * Duration(1, 6)


def test_Component_start_offset_22():
    r'''Offsets work on nested contexts.
    '''

    vin = Voice(notetools.make_repeated_notes(4))
    vout = Voice([Note(0, (1, 8)), vin])
    vin.name = vout.name = 'voice'
    staff = Staff([Note(1, (1, 8)), vout])
    assert vin.get_timespan().start_offset == Duration(2, 8)
    assert vout.get_timespan().start_offset == Duration(1, 8)


def test_Component_start_offset_23():
    r'''Offsets work on nested parallel contexts.
     '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([v1, v2])
    staff.is_parallel = True
    assert staff[0].get_timespan().start_offset == 0
    assert staff[1].get_timespan().start_offset == 0


def test_Component_start_offset_24():
    r'''Offsets works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v1b= Voice(notetools.make_repeated_notes(4))
    v2b= Voice(notetools.make_repeated_notes(4))
    v1.name = v1b.name = 'voiceOne'
    s1 = Staff([v1, v1b])
    s2 = Staff([v2, v2b])
    gs = scoretools.GrandStaff([s1, s2])
    assert v1.get_timespan().start_offset == 0
    assert v2.get_timespan().start_offset == 0
    assert v1b.get_timespan().start_offset == Duration(4, 8)
    assert v2b.get_timespan().start_offset == Duration(4, 8)
