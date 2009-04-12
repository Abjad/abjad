from abjad import *
from abjad.tools import construct


def test_construct_note_train_01( ):
   '''Construct train of 1/16th notes equal to 1/4 total duration.'''

   t = Voice(construct.note_train(0, Rational(1, 16), Rational(1, 4)))

   r'''
   \new Voice {
      c'16
      c'16
      c'16
      c'16
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n}"


def test_construct_note_train_02( ):
   '''Construct train of 1/16th notes equal to 9/32 total duration.'''

   t = Voice(construct.note_train(0, Rational(1, 16), Rational(9, 32)))

   r'''
   \new Voice {
      c'16
      c'16
      c'16
      c'16
      c'32
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'32\n}"


def test_construct_note_train_03( ):
   '''Construct train of 1/16th notes equal to only 1/128 total duration.'''

   t = Voice(construct.note_train(0, Rational(1, 16), Rational(1, 128)))

   r'''
   \new Voice {
      c'128
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'128\n}"


def test_construct_note_train_04( ):
   '''Construct train of 1/16th notes equal to 4/10 total duration.'''

   t = Voice(construct.note_train(0, Rational(1, 16), Rational(4, 10)))

   r'''
   \new Voice {
      c'16
      c'16
      c'16
      c'16
      c'16
      c'16
      \times 4/5 {
         c'32
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\tc'16\n\t\\times 4/5 {\n\t\tc'32\n\t}\n}"


def test_construct_note_train_04( ):
   '''Construct train of written 1/16th notes within measure of 5/18.'''

   t = RigidMeasure((5, 18), construct.note_train(
      0, Rational(1, 16), Rational(5, 18), prolation = Rational(16, 18)))

   r'''
      \time 5/18
      \scaleDurations #'(8 . 9) {
         c'16
         c'16
         c'16
         c'16
         c'16
      }
   '''

   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}"
