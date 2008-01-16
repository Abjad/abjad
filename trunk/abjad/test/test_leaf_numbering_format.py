from abjad import *


def test_format_leaf_numbering_01( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].formatter.number = True
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { 0 }\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8 ^ \markup { 0 }
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_format_leaf_numbering_02( ):
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].formatter.number = True
   staff.formatter.number = True
   assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { 0 }\n\tcs'8 ^ \\markup { 1 }\n\td'8 ^ \\markup { 2 }\n\tef'8 ^ \\markup { 3 }\n\te'8 ^ \\markup { 4 }\n\tf'8 ^ \\markup { 5 }\n\tfs'8 ^ \\markup { 6 }\n\tg'8 ^ \\markup { 7 }\n}"
   '''
   \new Staff {
           c'8 ^ \markup { 0 }
           cs'8 ^ \markup { 1 }
           d'8 ^ \markup { 2 }
           ef'8 ^ \markup { 3 }
           e'8 ^ \markup { 4 }
           f'8 ^ \markup { 5 }
           fs'8 ^ \markup { 6 }
           g'8 ^ \markup { 7 }
   }
   '''
