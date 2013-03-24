from abjad import *


def test_Component_start_offset_01():
    t = Voice(notetools.make_repeated_notes(16))
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_02():
    t = Staff(notetools.make_repeated_notes(16))
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_03():
    t = Staff(notetools.make_repeated_notes(16))
    t[10] = Rest((1, 8))
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_04():
    t = Staff(notetools.make_repeated_notes(16))
    t[10:10] = [Rest((1, 8))]
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_05():
    t = Staff(notetools.make_repeated_notes(16))
    t[10:12] = [Rest((1, 8))]
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_06():
    '''Offset works with voices.
    '''

    v1 = Voice(notetools.make_repeated_notes(16))
    v2 = Voice(notetools.make_repeated_notes(16))
    v1.name = v2.name = 'voice'
    t = Container([v1, v2])
    for i, x in enumerate(t.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_07():
    t = tuplettools.FixedDurationTuplet(Duration(1,4), notetools.make_repeated_notes(3))
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(1, 12)


def test_Component_start_offset_08():
    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
    offset = 0
    for x, d in zip(t.leaves, [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]):
        assert x.timespan.start_offset == offset
        offset += Duration(*d)


def test_Component_start_offset_09():
    '''Offset works on nested tuplets.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tp, Note("c'4")])
    offset = 0
    for x, d in zip(t.leaves, [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]):
        assert x.timespan.start_offset == offset
        offset += Duration(*d)


def test_Component_start_offset_10():
    '''Offset works with parallel structures.
    '''

    v1 = Voice(notetools.make_repeated_notes(16))
    v2 = Voice(notetools.make_repeated_notes(16))
    t = Staff([v1, v2])
    t.is_parallel = True
    for i, x in enumerate(v1):
        assert x.timespan.start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_11():
    '''Offset on leaves works in nested contexts.
    '''

    v = Voice(notetools.make_repeated_notes(4))
    t = Staff([Note(0, (1, 8)), v, Note(0, (1, 8))])
    for i, x in enumerate(t.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8)
    for i, x in enumerate(v.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8) + Duration(1, 8)


def test_Component_start_offset_12():
    '''Offset on leaves works in sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    t = Staff([v1, v2])
    for i, x in enumerate(v1.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_13():
    '''Offset on leaves works in nested parallel contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    t = Staff([v1, v2])
    t.is_parallel = True
    for i, x in enumerate(v1.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8)
    for i, x in enumerate(v2.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8)


def test_Component_start_offset_14():
    '''Offset on leaves works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    t = Staff([Container([v1, v2]), v3])
    t[0].is_parallel = True
    for i, x in enumerate(v3.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_15():
    '''Offset on leaves works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    t = Staff([v3, Container([v1, v2])])
    t[1].is_parallel = True
    for i, x in enumerate(v1.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8) + Duration(1, 2)
    for i, x in enumerate(v2.leaves):
        assert x.timespan.start_offset == i * Duration(1, 8) + Duration(1, 2)


def test_Component_start_offset_16():
    '''Offsets works on sequential voices.
    '''

    t = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    t[0].name = t[1].name = 'voice'
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(4, 8)


def test_Component_start_offset_17():
    '''Prolated offset does NOT go across sequential staves.
    '''

    t = Container([Staff(notetools.make_repeated_notes(4)), Staff(notetools.make_repeated_notes(4))])
    t[0].name = t[1].name = 'staff'
    assert t[0].timespan.start_offset == Duration(0)
    assert t[1].timespan.start_offset == Duration(1, 2)


def test_Component_start_offset_18():
    '''Offsets works with nested voices.
    '''

    t = Staff([Voice(notetools.make_repeated_notes(4)), Voice(notetools.make_repeated_notes(4))])
    for i, x in enumerate(t):
        assert x.timespan.start_offset == i * Duration(4, 8)


def test_Component_start_offset_19():
    '''Offsets works on sequential tuplets.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3)) * 3)
    assert t[0].timespan.start_offset == 0 * Duration(1, 4)
    assert t[1].timespan.start_offset == 1 * Duration(1, 4)
    assert t[2].timespan.start_offset == 2 * Duration(1, 4)


def test_Component_start_offset_20():
    '''Offsets work on tuplets between notes.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    t = Voice([Note(0, (1, 8)), tp, Note(0, (1, 8))])
    assert t[0].timespan.start_offset == 0 * Duration(1, 8)
    assert t[1].timespan.start_offset == 1 * Duration(1, 8)
    assert t[2].timespan.start_offset == 3 * Duration(1, 8)


def test_Component_start_offset_21():
    '''Offsets work on nested tuplets.
    '''

    tp = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tp, Note("c'4")])
    assert t[0].timespan.start_offset == 0 * Duration(1, 6)
    assert t[1].timespan.start_offset == 1 * Duration(1, 6)
    assert t[2].timespan.start_offset == 2 * Duration(1, 6)


def test_Component_start_offset_22():
    '''Offsets work on nested contexts.
    '''

    vin = Voice(notetools.make_repeated_notes(4))
    vout = Voice([Note(0, (1, 8)), vin])
    vin.name = vout.name = 'voice'
    t = Staff([Note(1, (1, 8)), vout])
    assert vin.timespan.start_offset == Duration(2, 8)
    assert vout.timespan.start_offset == Duration(1, 8)


def test_Component_start_offset_23():
    '''Offsets work on nested parallel contexts.
     '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    t = Staff([v1, v2])
    t.is_parallel = True
    assert t[0].timespan.start_offset == 0
    assert t[1].timespan.start_offset == 0


def test_Component_start_offset_24():
    '''Offsets works in nested parallel and sequential contexts.
    '''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v1b= Voice(notetools.make_repeated_notes(4))
    v2b= Voice(notetools.make_repeated_notes(4))
    v1.name = v1b.name = 'voiceOne'
    s1 = Staff([v1, v1b])
    s2 = Staff([v2, v2b])
    gs = scoretools.GrandStaff([s1, s2])
    assert v1.timespan.start_offset == 0
    assert v2.timespan.start_offset == 0
    assert v1b.timespan.start_offset == Duration(4, 8)
    assert v2b.timespan.start_offset == Duration(4, 8)
