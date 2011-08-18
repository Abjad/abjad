from abjad import *


def test_Staff___getitem___01():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], skiptools.Skip)
    assert isinstance(t[4], tuplettools.FixedDurationTuplet)
    assert isinstance(t[-5], Note)
    assert isinstance(t[-4], Rest)
    assert isinstance(t[-3], Chord)
    assert isinstance(t[-2], skiptools.Skip)
    assert isinstance(t[-1], tuplettools.FixedDurationTuplet)


def test_Staff___getitem___02():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[0:0]
    assert len(slice) == 0
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___03():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[0:1]
    assert len(slice) == 1
    assert isinstance(slice[0], Note)
    for x in t:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___04():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[-1:]
    assert len(slice) == 1
    assert isinstance(slice[0], tuplettools.FixedDurationTuplet)
    for x in slice:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___05():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[1:-1]
    assert len(slice) == 3
    assert isinstance(slice[0], Rest)
    assert isinstance(slice[1], Chord)
    assert isinstance(slice[2], skiptools.Skip)
    for x in slice:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___06():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[2:]
    assert len(slice) == 3
    assert isinstance(slice[0], Chord)
    assert isinstance(slice[1], skiptools.Skip)
    assert isinstance(slice[2], tuplettools.FixedDurationTuplet)
    for x in slice:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___07():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[:-2]
    assert len(slice) == 3
    assert isinstance(slice[0], Note)
    assert isinstance(slice[1], Rest)
    assert isinstance(slice[2], Chord)
    for x in slice:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)


def test_Staff___getitem___08():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert componenttools.is_well_formed_component(t)
    slice = t[:]
    assert len(slice) == 5
    assert isinstance(slice, list)
    assert isinstance(slice[0], Note)
    assert isinstance(slice[1], Rest)
    assert isinstance(slice[2], Chord)
    assert isinstance(slice[3], skiptools.Skip)
    assert isinstance(slice[4], tuplettools.FixedDurationTuplet)
    for x in slice:
        assert x._parentage.parent == t
    assert componenttools.is_well_formed_component(t)
