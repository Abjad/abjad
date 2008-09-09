from abjad import *
from py.test import raises


def test_lcopy_01( ):
   '''Staff > tuplet works fine.'''
   t = Staff([
      FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3),
      FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)])
   for i, leaf in enumerate(iterate(t, '_Leaf')):   
      leaf.pitch = i
   '''
   \new Staff {
           \times 2/3 {
                   c'8
                   cs'8
                   d'8
           }
           \times 2/3 {
                   ef'8
                   e'8
                   f'8
           }
   }
   '''
   staff = lcopy(t, 1, 5)
   assert isinstance(staff, Staff)
   assert staff.duration.prolated == Rational(4, 12)
   assert len(staff) == 2
   tuplet = staff[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   #assert tuplet.duration == Rational(2, 12)
   assert tuplet.duration.target == Rational(2, 12)
   assert tuplet.duration.prolated == Rational(1, 6)
   assert tuplet.duration.multiplier == Rational(2, 3)
   assert check(staff)
   '''
   \new Staff {
           \times 2/3 {
                   cs'8
                   d'8
           }
           \times 2/3 {
                   ef'8
                   e'8
           }
   }
   '''


def test_lcopy_02( ):
   '''Staff > voice > tuplet works fine.'''
   t = Staff([Voice([ 
      FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3),
      FixedDurationTuplet((1, 4), Note(0, (1, 8)) * 3)])])
   '''
   \new Staff {
           \new Voice {
                   \times 2/3 {
                           c'8
                           cs'8
                           d'8
                   }
                   \times 2/3 {
                           ef'8
                           e'8
                           f'8
                   }
           }
   }
   '''
   new = lcopy(t, 1, 5)
   assert isinstance(new, Staff)
   assert new.duration.prolated == Rational(4, 12)
   assert len(new) == 1
   assert isinstance(new[0], Voice)
   assert len(new[0]) == 2
   assert isinstance(new[0][0], FixedDurationTuplet)
   #assert new[0][0].duration == Rational(2, 12)
   assert new[0][0].duration.target == Rational(2, 12)
   assert len(new[0][0]) == 2
   assert isinstance(new[0][1], FixedDurationTuplet)
   #assert new[0][1].duration == Rational(2, 12)
   assert new[0][1].duration.target == Rational(2, 12)
   assert len(new[0][1]) == 2
   '''
   \new Staff {
           \new Voice {
                   \times 2/3 {
                           cs'8
                           d'8
                   }
                   \times 2/3 {
                           ef'8
                           e'8
                   }
           }
   }
   '''


def test_lcopy_03( ):
   '''Parallel containers do not admit lcopy( ).'''
   t = Staff([
      Voice(Note(0, (1, 4)) * 8),
      Voice(Note(0, (1, 4)) * 8)])
   t.brackets = 'double-angle'
   assert raises(AssertionError, 'lcopy(t, 1, 5)')


def test_lcopy_04( ):
   '''Works fine on voices nested inside parallel context.'''
   t = Staff([
      Voice(Note(0, (1, 4)) * 8),
      Voice(Note(0, (1, 4)) * 8)])
   t.brackets = 'double-angle'
   new = lcopy(t[0], 1, 7)
   assert isinstance(new, Voice)
   assert len(new) == 6
   assert new.duration.prolated == Rational(6, 4)


def test_lcopy_05( ):
   '''Measures withtout tuplet trim fine.'''
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   new = lcopy(t, 1, 3)
   assert isinstance(new, Measure)
   assert new.meter == (2, 4)
   assert len(new) == 2
   assert new.duration.prolated == Rational(2, 4)


def test_lcopy_05b( ):
   '''Score > staff > notes.'''
   score = Score([Staff(Note(0, (1, 4)) * 4)])
   t = score[0]
   new = lcopy(t, 1, 3)
   assert isinstance(new, Staff)
   assert len(new) == 2
   assert new.duration.prolated == Rational(2, 4)


def test_lcopy_06( ):
   '''Measures with tuplets trim fine, including nonbinary meters.'''
   t = Measure((4, 4), [FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)])
   new = lcopy(t, 1, 4)
   assert isinstance(new, Measure)
   assert new.meter == (3, 5)
   assert len(new) == 1
   tuplet = new[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   #assert tuplet.duration == Rational(3, 4)
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 5)
   assert tuplet.duration.multiplier == Rational(1)
   note = tuplet[0]
   assert isinstance(note, Note)
   assert note.duration == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 5)


def test_lcopy_07( ):
   '''Voice > measure > tuplet works fine.'''
   t = Voice([
      Measure((4, 4), [FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)])])
   new = lcopy(t, 1, 4)
   assert isinstance(new, Voice)
   assert len(new) == 1
   assert new.duration.prolated == Rational(3, 5)
   measure = new[0]
   assert isinstance(measure, Measure)
   assert measure.meter == (3, 5)
   assert len(measure) == 1
   assert measure.duration == Rational(3, 5)
   assert measure.duration.prolated == Rational(3, 5)
   tuplet = measure[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   #assert tuplet.duration == Rational(3, 4)
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 5)


def test_lcopy_08( ):
   '''Measures shrink down when we copy a partial tuplet.'''
   t = Measure((4, 4), FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   new = lcopy(t, 1)
   assert isinstance(new, Measure)
   assert new.meter == (5, 6)
   assert len(new) == 2
   tuplet = new[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   #assert tuplet.duration == Rational(2, 4)
   assert tuplet.duration.target == Rational(2, 4)
   assert tuplet.duration.prolated == Rational(2, 6)
   assert tuplet.duration.multiplier == Rational(1)
   tuplet = new[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   #assert tuplet.duration == Rational(3, 4)
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 6)
   assert tuplet.duration.multiplier == Rational(1)
   '''
        \time 5/6
            \times 1/1 {
                cs'4
                d'4
            }
            \times 1/1 {
                ef'4
                e'4
                f'4
            }
   '''


def test_lcopy_09( ):
   '''Yet another test.'''
   t = Staff(Measure((4, 4), Note(0, (1, 4)) * 4) * 3)
   staff = lcopy(t, 5, 7)
   assert isinstance(staff, Staff)
   assert len(staff) == 1
   measure = staff[0]
   assert isinstance(measure, Measure)
   assert measure.meter == (2, 4)
   assert len(measure) == 2
