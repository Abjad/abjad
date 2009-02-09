from abjad import *


def test_rigid_measure_trim_01( ):
   '''Nonnegative indices work.'''
   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(0)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)


def test_rigid_measure_trim_02( ):
   '''Negative indices work.'''
   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(-1)
   assert t.format == "\t\\time 3/8\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)
   

def test_rigid_measure_trim_03( ):
   '''Denominator preservation in meter.'''
   t = RigidMeasure((4, 8), Note(0, (1, 8)) * 4)
   t.trim(0, 2)
   assert t.format == "\t\\time 2/8\n\tc'8\n\tc'8"
   assert check(t)


def test_rigid_measure_trim_04( ):
   '''Denominator changes from 8 to 16.'''
   t = RigidMeasure((4, 8), Note(0, (1, 16)) * 2 + Note(0, (1, 8)) * 3)
   t.trim(0)
   assert t.format == "\t\\time 7/16\n\tc'16\n\tc'8\n\tc'8\n\tc'8"
   assert check(t)


def test_rigid_measure_trim_05( ):
   '''Trim nonbinary measure.'''
   t = RigidMeasure((4, 9), scale(4))
   t.trim(0)

   r'''
        \time 3/9
        d'8
        e'8
        f'8
   '''

   assert t.format == "\t\\time 3/9\n\td'8\n\te'8\n\tf'8"
   assert check(t)


def tet_rigid_measure_trim_06( ):
   '''Trim nonbinary measure, with denominator change.'''
   notes = scale(4)
   notes[0].duration.written = Rational(1, 16)
   notes[1].duration.written = Rational(1, 16)
   t = RigidMeasure((3, 9), notes)

   r'''
        \time 3/9
        c'16
        d'16
        e'8
        f'8
   '''

   t.trim(0)

   r'''
        \time 5/18
        d'16
        e'8
        f'8
   '''

   assert t.format == "\t\\time 5/18\n\td'16\n\te'8\n\tf'8"
   
