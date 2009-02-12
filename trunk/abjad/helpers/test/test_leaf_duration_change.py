from abjad import *


def test_leaf_duration_change_01( ):
   '''Change leaf to tied duration.'''

   t = Voice(scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaf_duration_change(t[1], Rational(5, 32))

   r'''
   \new Voice {
      c'8 [
      d'8 ~
      d'32 ]
      e'8
      f'8
   }
   '''

   assert check(t) 
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ~\n\td'32 ]\n\te'8\n\tf'8\n}"
   

def test_leaf_duration_change_02( ):
   '''Change leaf tied leaf to tied value;
      duplicate ties are not created.'''

   t = Voice(run(4))
   Tie(t[:2])
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [ ~
      c'8 ]
      c'8
      c'8
   }
   '''

   leaf_duration_change(t[1], Rational(5, 32))

   r'''
   \new Voice {
      c'8 [ ~
      c'8 ~
      c'32 ]
      c'8
      c'8
   }
   '''

   assert check(t)
   assert "\\new Voice {\n\tc'8 [ ~\n\tc'8 ~\n\tc'32 ]\n\tc'8\n\tc'8\n}"


def test_leaf_duration_change_03( ):
   '''Change leaf to nontied duration;
      same as t.duration.written = Rational(3, 16).'''

   t = Voice(scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaf_duration_change(t[1], Rational(3, 16))

   r'''
   \new Voice {
      c'8 [
      d'8. ]
      e'8
      f'8
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8. ]\n\te'8\n\tf'8\n}"
