from abjad import *


def test_lilyfiletools_make_basic_lily_file_01( ):


   score = Score([Staff(macros.scale(4))])
   lily_file = lilyfiletools.make_basic_lily_file(score)
   lily_file.header.composer = markuptools.Markup('Josquin')
   lily_file.layout.indent = 0
   lily_file.paper.top_margin = 15
   lily_file.paper.left_margin = 15

   r'''
   \header {
           composer = \markup { Josquin }
   }

   \layout {
           indent = #0
   }

   \paper {
           left-margin = #15
           top-margin = #15
   }

   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert score.lily_file is lily_file
   assert lily_file.music is score

   assert lily_file.format == "\\header {\n\tcomposer = \\markup { Josquin }\n}\n\n\\layout {\n\tindent = #0\n}\n\n\\paper {\n\tleft-margin = #15\n\ttop-margin = #15\n}\n\n\\new Score <<\n\t\\new Staff {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n>>"
