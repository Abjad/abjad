from abjad import *
import py.test


def test_breaks_interface_whitespace_01( ):
   '''Insert whitespace measure after measure.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
   Beam(t[2])
   Slur(t.leaves)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8 [ (
                   d'8 ]
           }
           {
                   \time 2/8
                   e'8 [
                   f'8 ]
           }
           {
                   \time 2/8
                   g'8 [
                   a'8 ] )
           }
   }
   '''

   t[1].breaks.whitespace = Rational(1, 32)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8 [ (
                   d'8 ]
           }
           {
                   \time 2/8
                   e'8 [
                   f'8 ]
                   {
                           \override Staff.TimeSignature #'stencil = ##f
                           \time 1/32
                           \stopStaff
                           s1 * 1/32
                           \startStaff
                           \revert Staff.TimeSignature #'stencil
                   }
           }
           {
                   \time 2/8
                   g'8 [
                   a'8 ] )
           }
   }
   '''

   assert check.wf(t)
   assert t.duration.prolated == Rational(3, 4)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ]\n\t\t{\n\t\t\t\\override Staff.TimeSignature #'stencil = ##f\n\t\t\t\\time 1/32\n\t\t\t\\stopStaff\n\t\t\ts1 * 1/32\n\t\t\t\\startStaff\n\t\t\t\\revert Staff.TimeSignature #'stencil\n\t\t}\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ] )\n\t}\n}"
   

def test_breaks_interface_whitespace_02( ):
   '''Whitespace after leaf raises TypographicWhitespaceError.
      Otherwise would confuse LilyPond timekeeping.'''

   t = RigidMeasure((2, 8), construct.scale(2))

   assert py.test.raises(
      TypographicWhitespaceError, 't[0].breaks.whitespace = Rational(1, 32)')
