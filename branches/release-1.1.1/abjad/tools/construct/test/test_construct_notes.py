from abjad import *
from abjad.tools import construct

def test_construct_notes_01( ):
   '''
   construct.notes can take a single pitch and a single duration.
   '''
   t = construct.notes(1, (1,4))
   assert isinstance(t, list)
   assert len(t) == 1
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(1, 4)
   assert not t[0].tie.spanned

def test_construct_notes_02( ):
   '''Tied durations result in more than one tied Note.'''
   t = construct.notes(1, (5, 8))
   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Note)
   assert t[0].duration.written == Rational(4, 8)
   assert t[1].duration.written == Rational(1, 8)
   assert t[0].tie.spanned
   assert t[1].tie.spanned

def test_construct_notes_03( ):
   '''
   construct.notes may take a list of pitches and a single duration.
   '''
   t = construct.notes([1, 2], (1, 4))
   assert len(t) == 2
   assert t[0].pitch.number == 1
   assert t[1].pitch.number == 2

def test_construct_notes_04( ):
   '''
   construct.notes may take a single pitch and a list of duration.
   '''
   t = construct.notes(1, [(1, 8), (1, 4)])
   assert len(t) == 2
   assert t[0].pitch.number == 1
   assert t[1].pitch.number == 1
   assert t[0].duration.written == Rational(1, 8)
   assert t[1].duration.written == Rational(1, 4)

def test_construct_notes_05( ):
   '''
   construct.notes may take a list of pitches and list of durations.
   '''
   t = construct.notes([0, 1], [(1, 8), (1, 4)])
   assert len(t) == 2
   assert t[0].pitch.number == 0
   assert t[1].pitch.number == 1
   assert t[0].duration.written == Rational(1, 8)
   assert t[1].duration.written == Rational(1, 4)


def test_construct_notes_06( ):
   '''
   Durations can be Rationals.
   '''
   t = construct.notes(1, Rational(1, 4))
   assert len(t) == 1
   assert t[0].duration.written == Rational(1, 4)

def test_construct_notes_07( ):
   '''
   Durations can be a list of Rationals.
   '''
   t = construct.notes(1, [Rational(1, 4)])
   assert len(t) == 1
   assert t[0].duration.written == Rational(1, 4)

def test_construct_notes_10( ):
   '''
   Key word 'direction' == 'big_endian' returns note durations in descending
   order. This is the default.
   '''
   t = construct.notes(1, (5, 16), direction='big-endian')
   assert len(t) == 2
   assert t[0].duration.written == Rational(4, 16)
   assert t[1].duration.written == Rational(1, 16)

def test_construct_notes_11( ):
   '''
   Key word 'direction' == 'little_endian' returns note durations in ascending
   order. 
   '''
   t = construct.notes(1, (5, 16), direction='little-endian')
   assert len(t) == 2
   assert t[0].duration.written == Rational(1, 16)
   assert t[1].duration.written == Rational(4, 16)


### PROLATED NOTES ###

def test_construct_notes_20( ):
   '''
   notes( ) can take parameters for a single prolated note.
   '''
   t = construct.notes(1, (1, 36))
   assert len(t) == 1
   assert isinstance(t[0], FixedMultiplierTuplet)
   assert len(t[0]) == 1
   assert t[0].duration.prolated == Rational(1, 36)
   assert t[0][0].duration.prolated == Rational(1, 36)
   assert t[0][0].duration.written == Rational(1, 32)


def test_construct_notes_21( ):
   '''
   notes( ) can take a single pitch and a list of prolated durations.
   '''
   t = construct.notes(1, [(1, 12), (1, 6), (1, 8)])
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


def test_construct_notes_22( ):
   '''
   notes( ) may take a direction attribute.
   '''
   t = construct.notes(1, [(5, 12), (1, 6), (1, 8)], \
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
