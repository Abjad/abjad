from abjad import *

def test_text_spanner_grob_handling_01( ):
   '''New attributes are formatted correctly.'''
   t = Staff(run(4))
   p = Text(t[:])
   p.font_shape = 'italic'
   assert t.format == "\\new Staff {\n\t\\override TextSpanner #'font-shape = #'italic\n\tc'8 \\startTextSpan\n\tc'8\n\tc'8\n\tc'8 \\stopTextSpan\n\t\\revert TextSpanner #'font-shape\n}"
   r'''
   \new Staff {
           \override TextSpanner #'font-shape = #'italic
           c'8 \startTextSpan
           c'8
           c'8
           c'8 \stopTextSpan
           \revert TextSpanner #'font-shape
   }
   '''
