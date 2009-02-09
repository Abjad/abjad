from abjad import *
from py.test import raises


### TODO: The syntax here is weird.
###       Change lcopy(expr, i, j) to lcopy(expr.leaves[i:j])?

def test_lcopy_01( ):
   '''Copy consecutive notes across tuplet boundary, in staff.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 2)
   diatonicize(t)

   r'''
   \new Staff {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   u = lcopy(t, 1, 5)

   r'''
   \new Staff {
           \times 2/3 {
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
           }
   }
   '''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\\times 2/3 {\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t}\n}"


def test_lcopy_02( ):
   '''Copy consecutive notes across tuplet boundary, in voice and staff.'''

   t = Staff([Voice(FixedDurationTuplet((2, 8), run(3)) * 2)])
   diatonicize(t)

   r'''
   \new Staff {
           \new Voice {
                   \times 2/3 {
                           c'8
                           d'8
                           e'8
                   }
                   \times 2/3 {
                           f'8
                           g'8
                           a'8
                   }
           }
   }
   '''
   
   u = lcopy(t, 1, 5)

   r'''
   \new Staff {
           \times 2/3 {
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
           }
   }
   '''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 2/3 {\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tf'8\n\t\t\tg'8\n\t\t}\n\t}\n}"


def test_lcopy_03( ):
   '''Copy leaves from sequential containers only.'''

   t = Staff(Voice(run(4)) * 2)
   diatonicize(t)
   t.brackets = 'double-angle'

   assert raises(ContiguityError, 'lcopy(t, 1, 5)')


def test_lcopy_04( ):
   '''Works fine on voices nested inside parallel context.'''

   t = Staff(Voice(run(4)) * 2)
   t.brackets = 'double-angle'
   diatonicize(t)

   r'''
   \new Staff <<
           \new Voice {
                   c'8
                   d'8
                   e'8
                   f'8
           }
           \new Voice {
                   g'8
                   a'8
                   b'8
                   c''8
           }
   >>
   '''

   u = lcopy(t[0], 1, 3)

   r'''
   \new Voice {
           d'8
           e'8
   }
   '''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Voice {\n\td'8\n\te'8\n}"


### TODO: The copy here winds up with each note in copy
###       wrapped in a trivial 1:1 tuplet.
###       Is there a way to NOT increase the depth of u?

def test_lcopy_05( ):
   '''RigidMeasures withtout tuplet trim fine.'''

   t = RigidMeasure((4, 8), scale(4))
   u = lcopy(t, 1, 3)

   assert isinstance(u, RigidMeasure)
   assert u.meter.forced == (2, 8)
   assert len(u) == 2
   assert u.duration.prolated == Rational(2, 8)


def test_lcopy_06( ):
   '''Score > staff > notes.'''
   score = Score([Staff(Note(0, (1, 4)) * 4)])
   t = score[0]
   new = lcopy(t, 1, 3)
   assert isinstance(new, Staff)
   assert len(new) == 2
   assert new.duration.prolated == Rational(2, 4)


def test_lcopy_07( ):
   '''RigidMeasures with tuplets trim fine, including nonbinary meters.'''
   t = RigidMeasure((4, 4), [FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)])
   new = lcopy(t, 1, 4)
   assert isinstance(new, RigidMeasure)
   assert new.meter.forced == (3, 5)
   assert len(new) == 1
   tuplet = new[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 5)
   assert tuplet.duration.multiplier == Rational(1)
   note = tuplet[0]
   assert isinstance(note, Note)
   assert note.duration.written == Rational(1, 4)
   assert note.duration.prolated == Rational(1, 5)


def test_lcopy_08( ):
   '''Voice > measure > tuplet works fine.'''
   t = Voice([
      RigidMeasure((4, 4), [FixedDurationTuplet((4, 4), Note(0, (1, 4)) * 5)])])
   new = lcopy(t, 1, 4)
   assert isinstance(new, Voice)
   assert len(new) == 1
   assert new.duration.prolated == Rational(3, 5)
   measure = new[0]
   assert isinstance(measure, RigidMeasure)
   assert measure.meter.forced == (3, 5)
   assert len(measure) == 1
   assert measure.duration.preprolated == Rational(3, 5)
   assert measure.duration.prolated == Rational(3, 5)
   tuplet = measure[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 5)


def test_lcopy_09( ):
   '''RigidMeasures shrink down when we copy a partial tuplet.'''
   t = RigidMeasure((4, 4), 
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3) * 2)
   new = lcopy(t, 1)
   assert isinstance(new, RigidMeasure)
   assert new.meter.forced == (5, 6)
   assert len(new) == 2
   tuplet = new[0]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 2
   assert tuplet.duration.target == Rational(2, 4)
   assert tuplet.duration.prolated == Rational(2, 6)
   assert tuplet.duration.multiplier == Rational(1)
   tuplet = new[1]
   assert isinstance(tuplet, FixedDurationTuplet)
   assert len(tuplet) == 3
   assert tuplet.duration.target == Rational(3, 4)
   assert tuplet.duration.prolated == Rational(3, 6)
   assert tuplet.duration.multiplier == Rational(1)
   r'''
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


def test_lcopy_10( ):
   '''Yet another test.'''
   t = Staff(RigidMeasure((4, 4), Note(0, (1, 4)) * 4) * 3)
   staff = lcopy(t, 5, 7)
   assert isinstance(staff, Staff)
   assert len(staff) == 1
   measure = staff[0]
   assert isinstance(measure, RigidMeasure)
   assert measure.meter.forced == (2, 4)
   assert len(measure) == 2
