from abjad import *
import py.test


def test_breaks_interface_eol_adjustment_01( ):
   '''Apply rightwards extra-offset to LilyPond TimeSignature
   and BarLine grobs.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[0])
   Beam(t[1])
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
                   f'8 ] )
           }
   }
   '''

   t[0].breaks.line = True
   t[0].breaks.eol_adjustment = True

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8 [ (
                   d'8 ]
                   \adjustEOLMeterBarlineExtraOffset
                   \break
           }
           {
                   \time 2/8
                   e'8 [
                   f'8 ] )
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t\t\\adjustEOLMeterBarlineExtraOffset\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_breaks_interface_eol_adjustment_02( ):
   '''Raise LineBreakError when attempting to set eol and
   no line break is present.
   '''

   t = Note(0, (1, 4))
   assert py.test.raises(LineBreakError, 't.breaks.eol_adjustment = True')
