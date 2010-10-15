from abjad import *


def test_Skip___init____01( ):
   '''Init skip from LilyPond input string.
   '''

   skip = skiptools.Skip('s8.')
   assert isinstance(skip, skiptools.Skip)


def test_Skip___init____02( ):
   '''Init skip from written duration and LilyPond multiplier.
   '''

   skip = skiptools.Skip((1, 4), (1, 2))

   assert isinstance(skip, skiptools.Skip)


def test_Skip___init____03( ):
   '''Init skip from containerize note.
   '''

   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   s = skiptools.Skip(c)
   assert isinstance(s, skiptools.Skip)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert s._parentage.parent is None
   assert s.duration.written == duration


def test_Skip___init____04( ):
   '''Init skip from tupletized note.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   skip = skiptools.Skip(t[0])
   assert isinstance(t[0], Chord)
   assert isinstance(skip, skiptools.Skip)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d
   assert skip._parentage.parent is None


def test_Skip___init____05( ):
   '''Init skip from beamed chord.
   '''

   t = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   spannertools.BeamSpanner(t[:])
   skip = skiptools.Skip(t[0])
   assert isinstance(t[0], Chord)
   assert isinstance(skip, skiptools.Skip)
   assert t[0]._parentage.parent is t
   assert skip._parentage.parent is None
