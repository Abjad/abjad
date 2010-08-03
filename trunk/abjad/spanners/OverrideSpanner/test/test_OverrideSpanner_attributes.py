from abjad import *


def test_OverrideSpanner_attributes_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[0], 'Beam', 'positions', (8, 8))

   r'''
   \new Staff {
      \once \override Beam #'positions = #'(8 . 8)
       c'8
       cs'8
       d'8
       ef'8
       e'8
       f'8
       fs'8
       g'8
   }
   '''

   assert repr(q) == "Override([c'8], Beam, positions, (8, 8))"
   assert str(q) == repr(q)
   assert len(q.components) == 1
   assert q.duration.prolated == Rational(1, 8)

   assert t.format == "\\new Staff {\n\t\\once \\override Beam #'positions = #'(8 . 8)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"


def test_OverrideSpanner_attributes_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   q = Override(t[ : 4], 'Beam', 'positions', (8, 8))

   r'''
   \new Staff {
      \override Beam #'positions = #'(8 . 8)
       c'8
       cs'8
       d'8
       ef'8
       \revert Beam #'positions
       e'8
       f'8
       fs'8
       g'8
   }
   '''

   assert repr(q) == "Override([c'8, cs'8, d'8, ef'8], Beam, positions, (8, 8))"
   assert str(q) == repr(q)
   assert len(q.components) == 4
   assert q.duration.prolated == Rational(1, 2)

   assert t.format == "\\new Staff {\n\t\\override Beam #'positions = #'(8 . 8)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\revert Beam #'positions\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
