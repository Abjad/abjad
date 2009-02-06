from abjad import *
from abjad.tools import construct

def test_notes_prolated_01( ):
   '''
   notes_prolated( ) can take parameters for a single note.
   '''
   t = construct.notes_prolated(1, (1, 8))
   assert len(t) == 1
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 8)


def test_notes_prolated_02( ):
   '''
   notes_prolated( ) can take parameters for a single prolated note.
   '''
   t = construct.notes_prolated(1, (1, 12))
   assert len(t) == 1
   assert isinstance(t[0], FixedMultiplierTuplet)
   assert len(t[0]) == 1
   assert t[0].duration.prolated == Rational(1, 12)
   assert t[0][0].duration.prolated == Rational(1, 12)
   assert t[0][0].duration.written == Rational(1, 8)


def test_notes_prolated_03( ):
   '''
   notes_prolated( ) can take a single pitch and a list of prolated durations.
   '''
   t = construct.notes_prolated(1, [(1, 12), (1, 6), (1, 8)])
   assert len(t) == 2
   assert isinstance(t[0], FixedMultiplierTuplet)
   assert isinstance(t[1], Note)
   assert len(t[0]) == 2
   assert t[0].duration.prolated == Rational(3, 12)
   assert t[0][0].duration.prolated == Rational(1, 12)
   assert t[0][1].duration.prolated == Rational(1, 6)
   assert t[0][0].duration.written == Rational(1, 8)
   assert t[0][1].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 8)
   r'''
   \times 2/3 {
           cs'8
           cs'4
   }
   cs'8
   '''


def test_notes_prolated_04( ):
   '''
   notes_prolated( ) may take a direction attribute.
   '''
   t = construct.notes_prolated(1, [(5, 12), (1, 6), (1, 8)], \
      direction='little-endian')
   assert len(t) == 2
   assert isinstance(t[0], FixedMultiplierTuplet)
   assert isinstance(t[1], Note)
   assert len(t[0]) == 3
   assert t[0].duration.prolated == Rational(7, 12)
   assert t[0][0].duration.prolated == Rational(1, 12)
   assert t[0][1].duration.prolated == Rational(4, 12)
   assert t[0][2].duration.prolated == Rational(1, 6)
   assert t[0][0].duration.written == Rational(1, 8)
   assert t[0][1].duration.written == Rational(4, 8)
   assert t[0][2].duration.written == Rational(1, 4)
   assert t[1].duration.written == Rational(1, 8)
