from abjad import *


def test_leaftools_duration_preprolated_change_01( ):
   '''Change leaf to tied duration.'''

   t = Voice(construct.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaftools.duration_preprolated_change(t[1], Rational(5, 32))

   r'''
   \new Voice {
      c'8 [
      d'8 ~
      d'32 ]
      e'8
      f'8
   }
   '''

   assert check.wf(t) 
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ~\n\td'32 ]\n\te'8\n\tf'8\n}"
   

def test_leaftools_duration_preprolated_change_02( ):
   '''Change tied leaf to tied value.
      Duplicate ties are not created.'''

   t = Voice(construct.run(4))
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

   leaftools.duration_preprolated_change(t[1], Rational(5, 32))

   r'''
   \new Voice {
      c'8 [ ~
      c'8 ~
      c'32 ]
      c'8
      c'8
   }
   '''

   assert check.wf(t)
   assert "\\new Voice {\n\tc'8 [ ~\n\tc'8 ~\n\tc'32 ]\n\tc'8\n\tc'8\n}"


def test_leaftools_duration_preprolated_change_03( ):
   '''Change leaf to nontied duration.
      Same as t.duration.written = Rational(3, 16).'''

   t = Voice(construct.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaftools.duration_preprolated_change(t[1], Rational(3, 16))

   r'''
   \new Voice {
      c'8 [
      d'8. ]
      e'8
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8. ]\n\te'8\n\tf'8\n}"


def test_leaftools_duration_preprolated_change_04( ):
   '''Change leaf to tied, nonbinary duration.
      FixedMultiplierTuplet inserted over new tied notes.'''

   t = Voice(construct.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaftools.duration_preprolated_change(t[1], Rational(5, 48))

   r'''
   \new Voice {
           c'8 [
           \times 2/3 {
                   d'8 ~
                   d'32 ]
           }
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'8 ~\n\t\td'32 ]\n\t}\n\te'8\n\tf'8\n}"


def test_leaftools_duration_preprolated_change_05( ):
   '''Change leaf to untied, nonbinary duration.
      FixedMultiplierTuplet inserted over input leaf.'''

   t = Voice(construct.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   leaftools.duration_preprolated_change(t[1], Rational(1, 12))

   r'''
   \new Voice {
           c'8 [
           \times 2/3 {
                   d'8 ]
           }
           e'8
           f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\t\\times 2/3 {\n\t\td'8 ]\n\t}\n\te'8\n\tf'8\n}" 


def test_leaftools_duration_preprolated_change_06( ):
   '''Change leaf with LilyPond multiplier to untied, binary duration.
      LilyPond multiplier changes but leaf written duration does not.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   leaftools.duration_preprolated_change(t, Rational(1, 32))

   assert check.wf(t)
   assert t.format == "c'8 * 1/4"


def test_leaftools_duration_preprolated_change_07( ):
   '''Change leaf with LilyPond multiplier to untied, binary duration.
      LilyPond multiplier changes but leaf written duration does not.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   leaftools.duration_preprolated_change(t, Rational(3, 32))

   assert check.wf(t)
   assert t.format == "c'8 * 3/4"


def test_leaftools_duration_preprolated_change_08( ):
   '''Change leaf with LilyPond multiplier to tied, binary duration.
      LilyPond multiplier changes but leaf written duration does not.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   leaftools.duration_preprolated_change(t, Rational(5, 32))

   assert check.wf(t)
   assert t.format == "c'8 * 5/4"


def test_leaftools_duration_preprolated_change_09( ):
   '''Change leaf with LilyPond multiplier to nonbinary duration.
      LilyPond multiplier changes but leaf written duration does not.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   leaftools.duration_preprolated_change(t, Rational(1, 24))

   assert check.wf(t)
   assert t.format == "c'8 * 1/3"


def test_leaftools_duration_preprolated_change_10( ):
   '''Change leaf with LilyPond multiplier.
      Change to nonbinary duration necessitating ties.
      LilyPond multiplier changes but leaf written duration does not.'''

   t = Note(0, (1, 8))
   t.duration.multiplier = Rational(1, 2)

   "c'8 * 1/2"

   leaftools.duration_preprolated_change(t, Rational(5, 24))

   assert check.wf(t)
   assert t.format == "c'8 * 5/3"
