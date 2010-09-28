from abjad import *
from py.test import raises


def test_Staff_append_01( ):
   '''Append one note.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Note(0, (1, 4)))
   assert componenttools.is_well_formed_component(t)
   assert len(t) == 5
   assert t.duration.contents == Fraction(5, 4)


def test_Staff_append_02( ):
   '''Append one chord.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(Chord([2, 3, 4], (1, 4)))
   assert componenttools.is_well_formed_component(t)
   assert len(t) == 5
   assert t.duration.contents == Fraction(5, 4)


def test_Staff_append_03( ):
   '''Append one tuplet.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(tuplettools.FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3))
   assert componenttools.is_well_formed_component(t)
   assert len(t) == 5
   assert t.duration.contents == Fraction(5, 4)


def test_Staff_append_04( ):
   '''Empty containers are allowed but not well-formed.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.append(tuplettools.FixedDurationTuplet((2, 8), [ ]))
   assert len(t) == 5
   assert t.duration.contents == Fraction(5, 4)
