from abjad import *
import py.test


def test_lcopy_01( ):
   '''Copy consecutive notes across tuplet boundary, in staff.'''

   t = Staff(FixedDurationTuplet((2, 8), run(3)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
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
   }'''

   u = lcopy(t, 1, 5)

   r'''\new Staff {
           \times 2/3 {
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
           }
   }'''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\\times 2/3 {\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t\tg'8\n\t}\n}"


def test_lcopy_02( ):
   '''Copy consecutive notes across tuplet boundary, in voice and staff.'''

   t = Staff([Voice(FixedDurationTuplet((2, 8), run(3)) * 2)])
   pitchtools.diatonicize(t)

   r'''\new Staff {
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
   }'''
   
   u = lcopy(t, 1, 5)

   r'''\new Staff {
           \times 2/3 {
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
           }
   }'''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 2/3 {\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tf'8\n\t\t\tg'8\n\t\t}\n\t}\n}"


def test_lcopy_03( ):
   '''Copy leaves from sequential containers only.'''

   t = Staff(Voice(run(4)) * 2)
   pitchtools.diatonicize(t)
   t.parallel = True

   assert py.test.raises(ContiguityError, 'lcopy(t, 1, 5)')


def test_lcopy_04( ):
   '''Works fine on voices nested inside parallel context.'''

   t = Staff(Voice(run(4)) * 2)
   t.parallel = True
   pitchtools.diatonicize(t)

   r'''\new Staff <<
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
   >>'''

   u = lcopy(t[0], 1, 3)

   r'''\new Voice {
           d'8
           e'8
   }'''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Voice {\n\td'8\n\te'8\n}"


def test_lcopy_05( ):
   '''Copy consecutive notes in binary measure.'''

   t = RigidMeasure((4, 8), scale(4))
   u = lcopy(t, 1, 3)

   r'''\time 2/8
        d'8
        e'8'''

   assert check(u)
   assert u.format == "\t\\time 2/8\n\td'8\n\te'8"


def test_lcopy_06( ):
   '''Copy consecutive notes in staff and score.'''

   score = Score([Staff(scale(4))])
   t = score[0]
   new = lcopy(t, 1, 3)

   r'''\new Staff {
           d'8
           e'8
   }'''
   
   assert check(t)
   assert check(new)
   assert new.format == "\\new Staff {\n\td'8\n\te'8\n}"


def test_lcopy_07( ):
   '''Copy consecutive leaves from tuplet in binary measure;
      nonbinary measure results.'''

   t = RigidMeasure((4, 8), [FixedDurationTuplet((4, 8), scale(5))])

   r'''\time 4/8
        \times 4/5 {
                c'8
                d'8
                e'8
                f'8
                g'8
        }'''

   u = lcopy(t, 1, 4)

   r'''\time 3/10
        \scaleDurations #'(4 . 5) {
                        d'8
                        e'8
                        f'8
        }'''

   assert check(t)
   assert check(u)
   assert u.format == "\t\\time 3/10\n\t\\scaleDurations #'(4 . 5) {\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t}"


def test_lcopy_08( ):
   '''Copy consecutive leaves from tuplet in measure and voice;
      nonbinary measure results.'''

   t = Voice([RigidMeasure((4, 8), [FixedDurationTuplet((4, 8), scale(5))])])
  
   r'''\new Voice {
                   \time 4/8
                   \times 4/5 {
                           c'8
                           d'8
                           e'8
                           f'8
                           g'8
                   }
   }'''

   u = lcopy(t, 1, 4)

   r'''\new Voice {
                   \time 3/10
                   \scaleDurations #'(4 . 5) {
                                   d'8
                                   e'8
                                   f'8
                   }
   }'''

   assert check(t)
   assert check(u)
   assert u.format == "\\new Voice {\n\t\t\\time 3/10\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\t\td'8\n\t\t\t\te'8\n\t\t\t\tf'8\n\t\t}\n}"


def test_lcopy_09( ):
   '''RigidMeasures shrink down when we copy a partial tuplet.'''

   t = RigidMeasure((4, 8), FixedDurationTuplet((2, 8), run(3)) * 2)
   pitchtools.diatonicize(t)

   r'''\time 4/8
        \times 2/3 {
                c'8
                d'8
                e'8
        }
        \times 2/3 {
                f'8
                g'8
                a'8
        }'''

   u = lcopy(t, 1)

   r'''\time 5/12
        \scaleDurations #'(2 . 3) {
                        d'8
                        e'8
                        f'8
                        g'8
                        a'8
        }'''

   assert check(t)
   assert check(u)
   assert u.format == "\t\\time 5/12\n\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8\n\t\t\te'8\n\t\t\tf'8\n\t\t\tg'8\n\t\t\ta'8\n\t}"


def test_lcopy_10( ):
   '''Copy consecutive leaves across measure boundary.'''

   t = Staff(RigidMeasure((3, 8), run(3)) * 2)
   pitchtools.diatonicize(t)

   r'''\new Staff {
                   \time 3/8
                   c'8
                   d'8
                   e'8
                   \time 3/8
                   f'8
                   g'8
                   a'8
   }'''

   u = lcopy(t, 2, 4)

   r'''\new Staff {
                   \time 1/8
                   e'8
                   \time 1/8
                   f'8
   }'''
   
   assert check(t)
   assert check(u)
   assert u.format == "\\new Staff {\n\t\t\\time 1/8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8\n}"
