from abjad import *


# TEST COPY ONE LEAF #

def test__Leaf___copy___01():
    m = Note(0, (1, 8))
    n = componenttools.copy_components_and_fracture_crossing_spanners([m])[0]
    assert id(m) != id(n)
    assert m._parentage.parent is None
    assert n._parentage.parent is None


def test__Leaf___copy___02():
    r = Rest((1, 8))
    s = componenttools.copy_components_and_fracture_crossing_spanners([r])[0]
    assert id(r) != id(s)
    assert r._parentage.parent is None
    assert s._parentage.parent is None


def test__Leaf___copy___03():
    s = skiptools.Skip((1, 8))
    t = componenttools.copy_components_and_fracture_crossing_spanners([s])[0]
    assert id(s) != id(t)
    assert s._parentage.parent is None
    assert t._parentage.parent is None


def test__Leaf___copy___04():
    d = Chord([2, 3, 4], (1, 4))
    e = componenttools.copy_components_and_fracture_crossing_spanners([d])[0]
    assert id(d) != id(e)
    assert d._parentage.parent is None
    assert e._parentage.parent is None


def test__Leaf___copy___05():
    t = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    m = t[1]
    n = componenttools.copy_components_and_fracture_crossing_spanners([m])[0]
    assert id(m) != id(n)
    assert m._parentage.parent is t
    assert n._parentage.parent is None


# TEST COPY ONE CONTAINER #

def test__Leaf___copy___06():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    u = componenttools.copy_components_and_fracture_crossing_spanners([t])[0]
    id(u) is not id(t)
    componenttools.is_well_formed_component(t)
    componenttools.is_well_formed_component(u)


# TEST COPY ONE TUPLETIZED NOTE #

def test__Leaf___copy___07():
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3) * 3)
    u = componenttools.copy_components_and_fracture_crossing_spanners(t.leaves[4:5])[0]
    assert isinstance(u, Note)
    assert u.written_pitch.numbered_chromatic_pitch == t.leaves[4].written_pitch.numbered_chromatic_pitch
    assert u.written_duration == t.leaves[4].written_duration
    assert id(u) != id(t.leaves[4])
    assert u.prolated_duration != t.leaves[4].prolated_duration


def test__Leaf___copy___08():
    t = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3) * 3)
    u = componenttools.copy_components_and_fracture_crossing_spanners(t.leaves[5:6])[0]
    assert isinstance(u, Note)
    assert u.written_pitch.numbered_chromatic_pitch == t.leaves[5].written_pitch.numbered_chromatic_pitch
    assert u.written_duration == t.leaves[5].written_duration
    assert id(u) != id(t.leaves[5])
    assert u.prolated_duration != t.leaves[5].prolated_duration
