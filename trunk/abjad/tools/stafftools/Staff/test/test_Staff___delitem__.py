from abjad import *
from py.test import raises


def test_Staff___delitem___01():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], skiptools.Skip)
    assert isinstance(t[4], tuplettools.FixedDurationTuplet)
    del(t[0])
    assert len(t) == 4
    assert isinstance(t[0], Rest)
    assert isinstance(t[1], Chord)
    assert isinstance(t[2], skiptools.Skip)
    assert isinstance(t[3], tuplettools.FixedDurationTuplet)
    del(t[0])
    assert len(t) == 3
    assert isinstance(t[0], Chord)
    assert isinstance(t[1], skiptools.Skip)
    assert isinstance(t[2], tuplettools.FixedDurationTuplet)
    del(t[0])
    assert len(t) == 2
    assert isinstance(t[0], skiptools.Skip)
    assert isinstance(t[1], tuplettools.FixedDurationTuplet)
    del(t[0])
    assert len(t) == 1
    assert isinstance(t[0], tuplettools.FixedDurationTuplet)
    del(t[0])
    assert len(t) == 0


def test_Staff___delitem___02():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], skiptools.Skip)
    assert isinstance(t[4], tuplettools.FixedDurationTuplet)
    del(t[-1])
    assert len(t) == 4
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], skiptools.Skip)
    del(t[-1])
    assert len(t) == 3
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    del(t[-1])
    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    del(t[-1])
    assert len(t) == 1
    assert isinstance(t[0], Note)
    del(t[-1])
    assert len(t) == 0


def test_Staff___delitem___03():
    t = Staff([Note("c'4"),
            Rest((1, 4)),
            Chord([2, 3, 4], (1, 4)),
            skiptools.Skip((1, 4)),
            tuplettools.FixedDurationTuplet(Duration(5, 16), Note(0, (1, 16)) * 4)])
    assert len(t) == 5
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], skiptools.Skip)
    assert isinstance(t[4], tuplettools.FixedDurationTuplet)
    del(t[3])
    assert len(t) == 4
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], Chord)
    assert isinstance(t[3], tuplettools.FixedDurationTuplet)
    del(t[-2])
    assert len(t) == 3
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    assert isinstance(t[2], tuplettools.FixedDurationTuplet)
    del(t[2])
    assert len(t) == 2
    assert isinstance(t[0], Note)
    assert isinstance(t[1], Rest)
    del(t[0])
    assert len(t) == 1
    assert isinstance(t[0], Rest)
    del(t[-1])
    assert len(t) == 0
