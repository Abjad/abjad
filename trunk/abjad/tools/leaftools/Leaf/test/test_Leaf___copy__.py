# -*- encoding: utf-8 -*-
from abjad import *


# TEST COPY ONE LEAF #

def test_Leaf___copy___01():
    m = Note(0, (1, 8))
    note_2 = componenttools.copy_components_and_fracture_crossing_spanners([m])[0]
    assert id(m) != id(note_2)
    assert m._parent is None
    assert note_2._parent is None


def test_Leaf___copy___02():
    rest_1 = Rest((1, 8))
    rest_2 = componenttools.copy_components_and_fracture_crossing_spanners([rest_1])[0]
    assert id(rest_1) != id(rest_2)
    assert rest_1._parent is None
    assert rest_2._parent is None


def test_Leaf___copy___03():
    skip = skiptools.Skip((1, 8))
    none = componenttools.copy_components_and_fracture_crossing_spanners([skip])[0]
    assert id(skip) != id(none)
    assert skip._parent is None
    assert none._parent is None


def test_Leaf___copy___04():
    d = Chord([2, 3, 4], (1, 4))
    e = componenttools.copy_components_and_fracture_crossing_spanners([d])[0]
    assert id(d) != id(e)
    assert d._parent is None
    assert e._parent is None


def test_Leaf___copy___05():
    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    m = tuplet[1]
    note_2 = componenttools.copy_components_and_fracture_crossing_spanners([m])[0]
    assert id(m) != id(note_2)
    assert m._parent is tuplet
    assert note_2._parent is None


# TEST COPY ONE CONTAINER #

def test_Leaf___copy___06():
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    u = componenttools.copy_components_and_fracture_crossing_spanners([staff])[0]
    id(u) is not id(staff)
    assert select(staff).is_well_formed()
    assert select(u).is_well_formed()


# TEST COPY ONE TUPLETIZED NOTE #

def test_Leaf___copy___07():
    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3) * 3)
    u = componenttools.copy_components_and_fracture_crossing_spanners(staff.select_leaves()[4:5])[0]
    assert isinstance(u, Note)
    assert u.written_pitch.numbered_chromatic_pitch == staff.select_leaves()[4].written_pitch.numbered_chromatic_pitch
    assert u.written_duration == staff.select_leaves()[4].written_duration
    assert id(u) != id(staff.select_leaves()[4])
    assert u.get_duration() != staff.select_leaves()[4].get_duration()


def test_Leaf___copy___08():
    staff = Staff(tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3) * 3)
    u = componenttools.copy_components_and_fracture_crossing_spanners(staff.select_leaves()[5:6])[0]
    assert isinstance(u, Note)
    assert u.written_pitch.numbered_chromatic_pitch == staff.select_leaves()[5].written_pitch.numbered_chromatic_pitch
    assert u.written_duration == staff.select_leaves()[5].written_duration
    assert id(u) != id(staff.select_leaves()[5])
    assert u.get_duration() != staff.select_leaves()[5].get_duration()
