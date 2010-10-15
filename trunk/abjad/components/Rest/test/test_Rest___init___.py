from abjad import *


def test_Rest___init____01( ):
   '''Init rest from LilyPond input string.
   '''

   rest = Rest('r8.')
   
   assert rest.duration.written == Fraction(3, 16)


def test_Rest___init____02( ):
   '''Init rest from written duration and LilyPond multiplier.
   '''

   rest = Rest(Fraction(1, 4), Fraction(1, 2))

   assert rest.format == 'r4 * 1/2'


def test_Rest___init____03( ):
   '''Init rest from other rest.
   '''

   rest_1 = Rest((1, 4), (1, 2))
   rest_1.override.staff.note_head.color = 'red'
   rest_2 = Rest(rest_1)

   assert isinstance(rest_1, Rest)
   assert isinstance(rest_2, Rest)
   assert rest_1 == rest_2
   assert rest_1 is not rest_2


def test_Rest___init____04( ):
   '''Init rest from containerized chord.
   '''

   c = Chord([2, 3, 4], (1, 4))
   duration = c.duration.written
   r = Rest(c)
   assert isinstance(r, Rest)
   # check that attributes have not been removed or added.
   assert dir(c) == dir(Chord([2, 3, 4], (1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r._parentage.parent is None
   assert r.duration.written == duration


def test_Rest___init____05( ):
   '''Init rest from tupletized chord.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), Chord([2, 3, 4], (1, 4)) * 3)
   d = t[0].duration.written
   rest = Rest(t[0])
   assert isinstance(rest, Rest)
   assert isinstance(t[0], Chord)
   assert t[0]._parentage.parent is t
   assert rest._parentage.parent is None


def test_Rest___init____06( ):
   '''Init rest from beamed chord.
   '''

   staff = Staff(Chord([2, 3, 4], (1, 4)) * 3)
   spannertools.BeamSpanner(staff[:])
   rest = Rest(staff[0])
   assert isinstance(rest, Rest)
   assert isinstance(staff[0], Chord)
   assert staff[0]._parentage.parent is staff
   assert rest._parentage.parent is None



def test_Rest___init____07( ):
   '''Init rest from skip.
   '''

   s = skiptools.Skip((1, 8))
   d = s.duration.written
   r = Rest(s)
   assert isinstance(r, Rest)
   assert dir(s) == dir(skiptools.Skip((1, 4)))
   assert dir(r) == dir(Rest((1, 4)))
   assert r._parentage.parent is None
   assert r.duration.written == d


def test_Rest___init____08( ):
   '''Init rest from tupletted skip.
   '''

   t = tuplettools.FixedDurationTuplet((2, 8), skiptools.Skip((1, 8)) * 3)
   d = t[0].duration.written
   rest = Rest(t[0])
   assert isinstance(t[0], skiptools.Skip)
   assert isinstance(rest, Rest)
   assert t[0]._parentage.parent is t
   assert t[0].duration.written == d
   assert rest._parentage.parent is None


def test_Rest___init____09( ):
   '''Init rest from beamed skip.
   '''

   t = Staff([Note(0, (1, 8)), skiptools.Skip((1, 8)), Note(0, (1, 8))])
   spannertools.BeamSpanner(t[:])
   rest = Rest(t[1])
   assert isinstance(t[1], skiptools.Skip)
   assert t[1] in t
   assert isinstance(rest, Rest)
   assert rest not in t
