from abjad import *


def test_measure_trim_by_count_01( ):
   '''Nonnegative indices work.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   measure_trim_by_count(t, 0)

   assert check(t)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"


def test_measure_trim_by_count_02( ):
   '''Negative indices work.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   measure_trim_by_count(t, -1)

   assert check(t)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"
   

def test_measure_trim_by_count_03( ):
   '''Denominator preservation in meter.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   measure_trim_by_count(t, 0, 2)

   assert check(t)
   assert t.format == "\t\\time 2/8\n\tc'8\n\tc'8"


def test_measure_trim_by_count_04( ):
   '''Denominator changes from 8 to 16.'''

   t = RigidMeasure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
   measure_trim_by_count(t, 0)

   assert check(t)
   assert t.format == "\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8"


def test_measure_trim_by_count_05( ):
   '''Trim nonbinary measure.'''

   t = RigidMeasure((4, 9), scale(4))
   measure_trim_by_count(t, 0)

   r'''\time 3/9
        \scaleDurations #'(8 . 9) {
                d'8
                e'8
                f'8
        }'''

   assert check(t)
   assert t.format == "\t\\time 3/9\n\t\\scaleDurations #'(8 . 9) {\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}"


def tet_rigid_measure_trim_06( ):
   '''Trim nonbinary measure, with denominator change.'''

   notes = scale(4)
   notes[0].duration.written = Rational(1, 16)
   notes[1].duration.written = Rational(1, 16)
   t = RigidMeasure((3, 9), notes)

   r'''\time 3/9
        \scaleDurations #'(8 . 9) {
                c'16
                d'16
                e'8
                f'8
        }'''

   measure_trim_by_count(t, 0)

   r'''\time 5/18
        \scaleDurations #'(8 . 9) {
                d'16
                e'8
                f'8
        }'''

   assert check(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\td'16\n\t\te'8\n\t\tf'8\n\t}"
