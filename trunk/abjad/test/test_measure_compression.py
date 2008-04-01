from abjad import *


def test_measure_compression_01( ):
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.append(Note(0, (1, 4)))
   assert t.duration == Rational(4, 4)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)
   assert check(t)
   assert t.format == "\t\\time 4/4\n\t\\compressMusic #'(4 . 5) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/4
        \compressMusic #'(4 . 5) {
                c'4
                c'4
                c'4
                c'4
                c'4
        }
   '''


def test_measure_compression_02( ):
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.extend(Note(0, (1, 4)) * 5)
   assert t.duration == Rational(4, 4)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 9)
   assert check(t)
   assert t.format == "\t\\time 4/4\n\t\\compressMusic #'(4 . 9) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/4
        \compressMusic #'(4 . 9) {
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
        }
   '''


def test_measure_compression_03( ):
   t = Measure((4, 4), Note(0, (1, 4)) * 4)
   t.pop( )
   assert t.duration == Rational(4, 4)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 3)
   assert check(t)
   assert t.format == "\t\\time 4/4\n\t\\compressMusic #'(4 . 3) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/4
        \compressMusic #'(4 . 3) {
                c'4
                c'4
                c'4
        }
   '''


def test_measure_compression_04( ):
   t = Measure((4, 5), Note(0, (1, 4)) * 4)
   t.append(Note(0, (1, 4)))
   assert t.duration == Rational(4, 5)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(4, 25)
   assert check(t)
   assert t.format == "\t\\time 4/5\n\t\\compressMusic #'(16 . 25) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/5
        \compressMusic #'(16 . 25) {
                c'4
                c'4                
                c'4
                c'4
                c'4
        }
   '''


def test_measure_compression_05( ):
   t = Measure((4, 5), Note(0, (1, 4)) * 4)
   t.extend(Note(0, (1, 4)) * 5)
   assert t.duration == Rational(4, 5)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(4, 45)
   assert check(t)
   assert t.format == "\t\\time 4/5\n\t\\compressMusic #'(16 . 45) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/5
        \compressMusic #'(16 . 45) {
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
                c'4
        }
   '''


def test_measure_compression_06( ):
   t = Measure((4, 5), Note(0, (1, 4)) * 4)
   t.pop( )
   assert t.duration == Rational(4, 5)
   assert t[0].duration == Rational(1, 4)
   assert t[0].duration.prolated == Rational(4, 15)
   assert check(t)
   assert t.format == "\t\\time 4/5\n\t\\compressMusic #'(16 . 15) {\n\t\tc'4\n\t\tc'4\n\t\tc'4\n\t}"
   '''
        \time 4/5
        \compressMusic #'(16 . 15) {
                c'4
                c'4
                c'4
        }
   '''
