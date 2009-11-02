from abjad import *


def test_slur_spanner_style_01( ):
   '''Slurs may be solid, dashed or dotted.'''

   t = Staff(construct.scale(4))
   slur = Slur(t[:])
   slur.style = 'solid'

   r'''
   \new Staff {
           \slurSolid
           c'8 (
           d'8
           e'8
           f'8 )
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\slurSolid\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"

   slur.style = None

   r'''
   \new Staff {
           c'8 (
           d'8
           e'8
           f'8 )
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"


def test_slur_spanner_style_02( ):
   '''Slurs may be solid, dashed or dotted.'''

   t = Staff(construct.scale(4))
   slur = Slur(t[:])
   slur.style = 'dotted'

   r'''
   \new Staff {
           \slurDotted
           c'8 (
           d'8
           e'8
           f'8 )
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\slurDotted\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"

   slur.style = None

   r'''
   \new Staff {
           c'8 (
           d'8
           e'8
           f'8 )
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
