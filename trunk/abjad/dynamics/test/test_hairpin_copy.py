from abjad import *


#def test_hairpin_copy_01( ):
#   '''Do not copy incomplete hairpins.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   Crescendo(staff[ : 4])
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   staff.append(staff[0].copy( ))
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tc'8\n}"
#   '''
#   \new Staff {
#           c'8 \<
#           cs'8
#           d'8
#           ef'8 \!
#           e'8
#           f'8
#           fs'8
#           g'8
#           c'8
#   }
#   '''


def test_hairpin_copy_02( ):
   '''Do copy complete hairpins.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   #staff.extend(staff.copy(0, 3))
   staff.extend(tcopy(staff[0:4]))
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n}"
   '''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
           c'8 \<
           cs'8
           d'8
           ef'8 \!
   }
   '''
