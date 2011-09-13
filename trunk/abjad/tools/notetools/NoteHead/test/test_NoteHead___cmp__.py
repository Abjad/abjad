from abjad import *


def test_NoteHead___cmp___01():

    p = notetools.NoteHead(12)
    q = notetools.NoteHead(12)

    assert not p <  q
    assert      p <= q
    assert      p == q
    assert not p != q
    assert not p >  q
    assert      p >= q


def test_NoteHead___cmp___02():

    p = notetools.NoteHead(12)
    q = notetools.NoteHead(13)

    assert not q <  p
    assert not q <= p
    assert not q == p
    assert      q != p
    assert      q >  p
    assert      q >= p


def test_NoteHead___cmp___03():

    p = notetools.NoteHead(12)
    q = 12

    assert not p <  q
    assert      p <= q
    assert      p == q
    assert not p != q
    assert not p >  q
    assert      p >= q


def test_NoteHead___cmp___04():

    p = notetools.NoteHead(12)
    q = 13

    assert not q <  p
    assert not q <= p
    assert not q == p
    assert      q != p
    assert      q >  p
    assert      q >= p
