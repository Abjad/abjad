from abjad import *


def test_beam_complex_durated_lone_01( ):
   '''BeamComplexDurated with lone = True applies beam 
      to a lone note at format-time.'''

   t = Voice(construct.scale(1))
   BeamComplexDurated(t, lone = True)

   r'''\new Voice {
      c'8 [ ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [ ]\n}"


def test_beam_complex_durated_lone_02( ):
   '''BeamComplexDurated with lone = False does not apply beam
      to a lone note at format-time.'''

   t = Voice(construct.scale(1))
   BeamComplexDurated(t, lone = False)

   r'''\new Voice {
      c'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8\n}"


def test_beam_complex_durated_lone_03( ):
   '''BeamComplexDurated with multiple leaves ignores 'lone' setting.'''

   t = Voice(construct.scale(2))
   BeamComplexDurated(t, lone = False)

   r'''\new Voice {
      \set stemLeftBeamCount = #0
      \set stemRightBeamCount = #1
      c'8 [
      \set stemLeftBeamCount = #1
      \set stemRightBeamCount = #0
      d'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\set stemLeftBeamCount = #0\n\t\\set stemRightBeamCount = #1\n\tc'8 [\n\t\\set stemLeftBeamCount = #1\n\t\\set stemRightBeamCount = #0\n\td'8 ]\n}"
