from abjad import *


def test_label_leaf_pcs_01( ):
   '''With number = True.'''

   t = Staff(construct.scale(4))
   label.leaf_pcs(t, number = True)

   r'''
   \new Staff {
      c'8 _ \markup { \small 0 }
      d'8 _ \markup { \small 2 }
      e'8 _ \markup { \small 4 }
      f'8 _ \markup { \small 5 }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 _ \\markup { \\small 0 }\n\td'8 _ \\markup { \\small 2 }\n\te'8 _ \\markup { \\small 4 }\n\tf'8 _ \\markup { \\small 5 }\n}"


def test_label_leaf_pcs_02( ):
   '''With color = True.'''

   t = Staff(construct.scale(4))
   label.leaf_pcs(t, number = False, color = True)

   r'''
   \new Staff {
      \once \override NoteHead #'color = #(x11-color 'red)
      c'8
      \once \override NoteHead #'color = #(x11-color 'orange)
      d'8
      \once \override NoteHead #'color = #(x11-color 'ForestGreen)
      e'8
      \once \override NoteHead #'color = #(x11-color 'MediumOrchid)
      f'8
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\once \\override NoteHead #'color = #(x11-color 'red)\n\tc'8\n\t\\once \\override NoteHead #'color = #(x11-color 'orange)\n\td'8\n\t\\once \\override NoteHead #'color = #(x11-color 'ForestGreen)\n\te'8\n\t\\once \\override NoteHead #'color = #(x11-color 'MediumOrchid)\n\tf'8\n}"
