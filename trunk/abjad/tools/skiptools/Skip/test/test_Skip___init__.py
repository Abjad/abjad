from abjad import *


def test_Skip___init___01():
    '''Init skip from LilyPond input string.
    '''

    skip = skiptools.Skip('s8.')
    assert isinstance(skip, skiptools.Skip)


def test_Skip___init___02():
    '''Init skip from written duration and LilyPond multiplier.
    '''

    skip = skiptools.Skip((1, 4), (1, 2))

    assert isinstance(skip, skiptools.Skip)


def test_Skip___init___03():
    '''Init skip from containerize note.
    '''

    c = Chord([2, 3, 4], (1, 4))
    duration = c.written_duration
    s = skiptools.Skip(c)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s._parentage.parent is None
    assert s.written_duration == duration


def test_Skip___init___04():
    '''Init skip from tupletized note.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Chord([2, 3, 4], (1, 4)) * 3)
    d = t[0].written_duration
    skip = skiptools.Skip(t[0])
    assert isinstance(t[0], Chord)
    assert isinstance(skip, skiptools.Skip)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d
    assert skip._parentage.parent is None


def test_Skip___init___05():
    '''Init skip from beamed chord.
    '''

    t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
    spannertools.BeamSpanner(t[:])
    skip = skiptools.Skip(t[0])
    assert isinstance(t[0], Chord)
    assert isinstance(skip, skiptools.Skip)
    assert t[0]._parentage.parent is t
    assert skip._parentage.parent is None


def test_Skip___init___06():
    n = Note(2, (1, 8))
    d = n.written_duration
    s = skiptools.Skip(n)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(n) == dir(Note("c'4"))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s.format == 's8'
    assert s._parentage.parent is None
    assert s.written_duration == d


def test_Skip___init___07():
    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    d = t[0].written_duration
    skip = skiptools.Skip(t[0])
    assert isinstance(t[0], Note)
    assert isinstance(skip, skiptools.Skip)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d


def test_Skip___init___08():
    '''Init skip from beamed note.
    '''

    t = Staff(Note(0, (1, 8)) * 3)
    spannertools.BeamSpanner(t[:])
    skip = skiptools.Skip(t[0])
    assert isinstance(t[0], Note)
    assert isinstance(skip, skiptools.Skip)
    assert t[0]._parentage.parent is t


def test_Skip___init___09():
    '''Init skip from unincorporaed rest.
    '''

    r = Rest((1, 8))
    d = r.written_duration
    s = skiptools.Skip(r)
    assert isinstance(s, skiptools.Skip)
    # check that attributes have not been removed or added.
    assert dir(r) == dir(Rest((1, 4)))
    assert dir(s) == dir(skiptools.Skip((1, 4)))
    assert s._parentage.parent is None
    assert s.written_duration == d


def test_Skip___init___10():
    '''Init skip from tupletized rest.
    '''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Rest((1, 8)) * 3)
    d = t[0].written_duration
    skip = skiptools.Skip(t[0])
    assert isinstance(skip, skiptools.Skip)
    assert isinstance(t[0], Rest)
    assert t[0]._parentage.parent is t
    assert t[0].written_duration == d
    assert skip._parentage.parent is None


def test_Skip___init___11():
    '''Init skip from spanned rest.
    '''

    t = Staff([Note(0, (1, 8)), Rest((1, 8)), Note(0, (1, 8))])
    spannertools.BeamSpanner(t[:])
    skip = skiptools.Skip(t[1])
    assert isinstance(skip, skiptools.Skip)
    assert isinstance(t[1], Rest)
    assert t[1]._parentage.parent is t
    assert skip._parentage.parent is None
