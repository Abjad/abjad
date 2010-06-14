from abjad import *


def test_rigid_measure_del_01( ):
   '''Nonnegative indices work.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   del(t[:1])

   assert check.wf(t)
   assert t.format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"


def test_rigid_measure_del_02( ):
   '''Negative indices work.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   del(t[-1:])

   assert check.wf(t)
   assert t.format == "{\n\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8\n}"
   

def test_rigid_measure_del_03( ):
   '''Denominator preservation in meter.'''

   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   del(t[:2])

   assert check.wf(t)
   assert t.format == "{\n\t\\time 2/8\n\tc'8\n\tc'8\n}"


def test_rigid_measure_del_04( ):
   '''Denominator changes from 8 to 16.'''

   t = RigidMeasure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
   del(t[:1])

   assert check.wf(t)
   assert t.format == "{\n\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8\n}"


def test_rigid_measure_del_05( ):
   '''Trim nonbinary measure.'''

   t = RigidMeasure((4, 9), leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   del(t[:1]) 

   r'''
   {
           \time 3/9
           \scaleDurations #'(8 . 9) {
                   d'8
                   e'8
                   f'8
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "{\n\t\\time 3/9\n\t\\scaleDurations #'(8 . 9) {\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"


def tet_rigid_measure_trim_06( ):
   '''Trim nonbinary measure, with denominator change.'''

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)
   notes[0].duration.written = Rational(1, 16)
   notes[1].duration.written = Rational(1, 16)
   t = RigidMeasure((3, 9), notes)

   r'''
   {
           \time 3/9
           \scaleDurations #'(8 . 9) {
                   c'16
                   d'16
                   e'8
                   f'8
           }
   }
   '''

   del(t[:1])

   r'''
   {
           \time 5/18
           \scaleDurations #'(8 . 9) {
                   d'16
                   e'8
                   f'8
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "{\n\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\td'16\n\t\te'8\n\t\tf'8\n\t}\n}"
