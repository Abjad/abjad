from abjad import *


def test_measures_concentrate_01( ):
   '''Concentrate one measure three times.
      Meter 3/8 goes to 9/24.
      Numerator and denominator both triple.'''

   t = RigidMeasure((3, 8), scale(3))
   Beam(t[:])
   measures_concentrate(t, [(3, 3)])

   r'''
        \time 9/24
        \scaleDurations #'(2 . 3) {
                c'16 [
                d'16
                e'16 ]
                c'16 [
                d'16
                e'16 ]
                c'16 [
                d'16
                e'16 ]
        }
   '''

   assert check.wf(t)
   assert t.format == "\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t}"


def test_measures_concentrate_02( ):
   '''Concentrate one measure four times over five.
      Meter 3/16 goes to 12/80.
      Numerator quadruples and denominator quintuples.'''

   t = RigidMeasure((3, 16), scale(3, Rational(1, 16)))
   Beam(t[:])
   measures_concentrate(t, [(4, 5)])

   r'''
        \time 12/80
        \scaleDurations #'(4 . 5) {
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
                c'64 [
                d'64
                e'64 ]
        }
   '''

   assert check.wf(t)
   assert t.format == "\t\\time 12/80\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t}"


def test_measures_concentrate_03( ):
   '''Concentrate one measure four times over four.
      Meter 3/16 goes to 12/64.
      Numerator and denominator both quadruple.'''

   t = RigidMeasure((3, 16), scale(3, Rational(1, 16)))
   Beam(t[:])
   measures_concentrate(t, [(4, 4)])

   r'''
        \time 12/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
   '''

   assert check.wf(t)
   assert t.format == "\t\\time 12/64\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]"


def test_measures_concentrate_04( ):
   '''Concentrate one measure two times over four.
      Meter 3/16 goes to 6/64.
      Numerator doubles and denominator quadruples.'''

   t = RigidMeasure((3, 16), scale(3, Rational(1, 16)))
   Beam(t[:])
   measures_concentrate(t, [(2, 4)])

   r'''
        \time 6/64
        c'64 [
        d'64
        e'64 ]
        c'64 [
        d'64
        e'64 ]
   '''

   assert check.wf(t)
   assert t.format == "\t\\time 6/64\n\tc'64 [\n\td'64\n\te'64 ]\n\tc'64 [\n\td'64\n\te'64 ]"
