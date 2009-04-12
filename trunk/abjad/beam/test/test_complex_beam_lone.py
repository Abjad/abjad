from abjad import *


def test_complex_beam_lone_01( ):
   '''ComplexBeam with lone = True applies beam 
      to a lone note at format-time.'''

   t = Voice(scale(1))
   ComplexBeam(t, lone = True)

   r'''
   \new Voice {
      c'8 [ ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ ]\n}"


def test_complex_beam_lone_02( ):
   '''ComplexBeam with lone = False does not apply beam
      to a lone note at format-time.'''

   t = Voice(scale(1))
   ComplexBeam(t, lone = False)

   r'''
   \new Voice {
      c'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8\n}"


def test_complex_beam_lone_03( ):
   '''ComplexBeam with multiple leaves ignores 'lone' setting.'''

   t = Voice(scale(2))
   ComplexBeam(t, lone = False)

   r'''
   \new Voice {
      \set stemLeftBeamCount = #0
      \set stemRightBeamCount = #1
      c'8 [
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #0
      d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #1\n\tc'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #0\n\td'8 ]\n}"
