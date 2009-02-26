from abjad import *


def test_measure_scale_and_remeter_01( ):
   '''Scale binary to nonbinary; no notehead rewriting necessary.'''

   t = RigidMeasure((3, 8), scale(3))
   measure_scale_and_remeter(t, Rational(2, 3))

   r'''
        \time 3/12
        \scaleDurations #'(2 . 3) {
                c'8
                d'8
                e'8
        }
   '''

   assert check(t)
   assert t.format == "\t\\time 3/12\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}"


def test_measure_scale_and_remeter_02( ):
   '''Scale nonbinary meter to binary; no notehead rewriting necessary.'''
  
   t = RigidMeasure((3, 12), scale(3))
   measure_scale_and_remeter(t, Rational(3, 2))

   r'''
        \time 3/8
        c'8
        d'8
        e'8
   '''

   assert check(t)
   assert t.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"


def test_measure_scale_and_remeter_03( ):
   '''Scale binary meter to binary meter; 
      noteheads rewrite with dots.'''

   t = RigidMeasure((3, 8), scale(3))
   measure_scale_and_remeter(t, Rational(3, 2))

   r'''
        \time 9/16
        c'8.
        d'8.
        e'8.
   '''

   assert check(t)
   assert t.format == "\t\\time 9/16\n\tc'8.\n\td'8.\n\te'8."


def test_measure_scale_and_remeter_04( ):
   '''Scale binary meter to binary meter;
      noteheads rewrite without dots.'''

   t = RigidMeasure((9, 16), scale(3, Rational(3, 16)))
   measure_scale_and_remeter(t, Rational(2, 3))

   r'''
        \time 3/8
        c'8
        d'8
        e'8
   '''

   assert check(t)
   assert t.format == "\t\\time 3/8\n\tc'8\n\td'8\n\te'8"


def test_measure_scale_and_remeter_05( ):
   '''Scale binary meter to nonbinary meter;
      no notehead rewriting necessary.'''

   t = RigidMeasure((9, 16), scale(9, Rational(1, 16)))
   measure_scale_and_remeter(t, Rational(2, 3))

   r'''
        \time 9/24
        \scaleDurations #'(2 . 3) {
                c'16
                d'16
                e'16
                f'16
                g'16
                a'16
                b'16
                c''16
                d''16
        }
   '''

   assert check(t)
   assert t.format == "\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16\n\t\td'16\n\t\te'16\n\t\tf'16\n\t\tg'16\n\t\ta'16\n\t\tb'16\n\t\tc''16\n\t\td''16\n\t}"


def test_measure_scale_and_remeter_06( ):
   '''Scale nonbinary meter to binary meter.
      noteheads rewrite with double duration.'''

   t = RigidMeasure((3, 12), scale(3))
   measure_scale_and_remeter(t, Rational(3))

   r'''
        \time 3/4
        c'4
        d'4
        e'4
   '''

   assert check(t)
   assert t.format == "\t\\time 3/4\n\tc'4\n\td'4\n\te'4"
