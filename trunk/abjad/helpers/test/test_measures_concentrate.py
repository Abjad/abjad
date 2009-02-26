from abjad import *


def test_measures_concentrate_01( ):
   '''Concentrate one measure three times.'''

   t = RigidMeasure((3, 8), scale(3))
   Beam(t[:])
   measures_concentrate(t, (3, 3))

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

   assert check(t)
   assert t.format == "\t\\time 9/24\n\t\\scaleDurations #'(2 . 3) {\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t\tc'16 [\n\t\td'16\n\t\te'16 ]\n\t}"


def test_measures_concentrate_02( ):
   '''Concentrate one measure four times over five.'''

   t = RigidMeasure((3, 16), scale(3, Rational(1, 16)))
   Beam(t[:])
   measures_concentrate(t, (4, 5))

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

   assert check(t)
   assert t.format == "\t\\time 12/80\n\t\\scaleDurations #'(4 . 5) {\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t\tc'64 [\n\t\td'64\n\t\te'64 ]\n\t}"
